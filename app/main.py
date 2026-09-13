import asyncio
import os
import re
import socket
import time
from typing import Dict, Any, List
from contextlib import asynccontextmanager

from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.responses import HTMLResponse, StreamingResponse
from fastapi.templating import Jinja2Templates
from starlette.requests import Request
import httpx

PRINTER_IP = os.getenv("PRINTER_IP", "192.168.50.99")
PRINTER_PORT = int(os.getenv("PRINTER_PORT", "8899"))
CAMERA_URL = os.getenv("CAMERA_URL", f"http://{PRINTER_IP}:8080/?action=stream")
POLL_INTERVAL = float(os.getenv("POLL_INTERVAL", "1.5"))

# Global cached state
latest_state: Dict[str, Any] = {
    "connected": False,
    "machine_type": "Flashforge Adventurer 5M Pro",
    "machine_name": "SNMOMF9201919",
    "firmware": "Unknown",
    "sn": "Unknown",
    "mac": "Unknown",
    "build_volume": {"x": 220, "y": 220, "z": 220},
    "machine_status": "OFFLINE",
    "move_mode": "IDLE",
    "current_file": "None",
    "material": "Unknown",
    "layer_height": "Unknown",
    "print_duration": "Unknown",
    "led_on": False,
    "nozzle_temp": 0.0,
    "nozzle_target": 0.0,
    "bed_temp": 0.0,
    "bed_target": 0.0,
    "current_layer": 0,
    "total_layers": 0,
    "progress_pct": 0,
    "sd_byte_pct": 0,
    "coords": {"x": 0.0, "y": 0.0, "z": 0.0, "a": 0.0, "b": 0.0},
    "last_update": 0,
    "error": None
}

connected_websockets: List[WebSocket] = []

def parse_filename_meta(filename: str):
    """
    Extracts metadata from filename e.g. Modular_SingleBay_16mm_M3_PLA_1h36m.gcode.3mf
    """
    meta = {"material": "Unknown", "duration": "Unknown"}
    if not filename or filename == "None":
        return meta
        
    for mat in ["PLA-CF", "PETG-CF", "ABS", "ASA", "TPU", "PLA", "PETG", "PC", "PA"]:
        if mat in filename.upper():
            meta["material"] = mat
            break
            
    dur_m = re.search(r"(\d+h\d+m|\d+m\d+s|\d+h|\d+m)", filename)
    if dur_m:
        meta["duration"] = dur_m.group(1)
        
    return meta

def query_printer_sync(ip: str, port: int) -> Dict[str, Any]:
    global latest_state
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(2.0)
        s.connect((ip, port))
        
        # We query info (~M115 once in a while or initial, ~M119, ~M105, ~M27, ~M114)
        cmds = ["~M115\r\n", "~M119\r\n", "~M105\r\n", "~M27\r\n", "~M114\r\n"]
        raw = {}
        for c in cmds:
            s.sendall(c.encode("ascii"))
            time.sleep(0.04)
            data = s.recv(2048).decode("latin1", errors="ignore")
            raw[c.strip()] = data
            
        s.close()
        
        # Parse M115 (Static machine specs)
        m115 = raw.get("~M115", "")
        m_type = re.search(r"Machine Type:\s*(.+)", m115)
        if m_type: latest_state["machine_type"] = m_type.group(1).strip()
        m_fw = re.search(r"Firmware:\s*(.+)", m115)
        if m_fw: latest_state["firmware"] = m_fw.group(1).strip()
        m_sn = re.search(r"SN:\s*(.+)", m115)
        if m_sn: latest_state["sn"] = m_sn.group(1).strip()
        m_mac = re.search(r"Mac Address:\s*([0-9A-Fa-f:]+)", m115)
        if m_mac: latest_state["mac"] = m_mac.group(1).strip()
        
        # Parse M119 (Status, File, LED)
        m119 = raw.get("~M119", "")
        m_stat = re.search(r"MachineStatus:\s*([A-Za-z0-9_]+)", m119)
        if m_stat: latest_state["machine_status"] = m_stat.group(1).strip()
        m_mode = re.search(r"MoveMode:\s*([A-Za-z0-9_]+)", m119)
        if m_mode: latest_state["move_mode"] = m_mode.group(1).strip()
        m_led = re.search(r"LED:\s*(\d+)", m119)
        if m_led: latest_state["led_on"] = (m_led.group(1) == "1")
        m_file = re.search(r"CurrentFile:\s*(.+)", m119)
        if m_file:
            cur_file = m_file.group(1).strip()
            latest_state["current_file"] = cur_file
            meta = parse_filename_meta(cur_file)
            latest_state["material"] = meta["material"]
            latest_state["print_duration"] = meta["duration"]
            
        # Parse M105 (Temps)
        m105 = raw.get("~M105", "")
        m_nozzle = re.search(r"T0:([\d\.]+)/([\d\.]+)", m105)
        if m_nozzle:
            latest_state["nozzle_temp"] = float(m_nozzle.group(1))
            latest_state["nozzle_target"] = float(m_nozzle.group(2))
        m_bed = re.search(r"B:([\d\.]+)/([\d\.]+)", m105)
        if m_bed:
            latest_state["bed_temp"] = float(m_bed.group(1))
            latest_state["bed_target"] = float(m_bed.group(2))
            
        # Parse M27 (Progress & Layers)
        m27 = raw.get("~M27", "")
        m_byte = re.search(r"SD printing byte (\d+)/100", m27)
        if m_byte:
            latest_state["sd_byte_pct"] = int(m_byte.group(1))
        m_layer = re.search(r"Layer:\s*(\d+)/(\d+)", m27)
        if m_layer:
            latest_state["current_layer"] = int(m_layer.group(1))
            latest_state["total_layers"] = int(m_layer.group(2))
            if latest_state["total_layers"] > 0:
                l_pct = int(round((latest_state["current_layer"] / latest_state["total_layers"]) * 100))
                latest_state["progress_pct"] = max(l_pct, latest_state["sd_byte_pct"])
            else:
                latest_state["progress_pct"] = latest_state["sd_byte_pct"]
        else:
            latest_state["progress_pct"] = latest_state["sd_byte_pct"]
            
        # Parse M114 (XYZ Coordinates)
        m114 = raw.get("~M114", "")
        m_coords = re.search(r"X:([-\d\.]+)\s+Y:([-\d\.]+)\s+Z:([-\d\.]+)\s+A:([-\d\.]+)\s+B:([-\d\.]+)", m114)
        if m_coords:
            latest_state["coords"] = {
                "x": float(m_coords.group(1)),
                "y": float(m_coords.group(2)),
                "z": float(m_coords.group(3)),
                "a": float(m_coords.group(4)),
                "b": float(m_coords.group(5))
            }
            
        latest_state["connected"] = True
        latest_state["error"] = None
        latest_state["last_update"] = time.time()
    except Exception as e:
        latest_state["connected"] = False
        latest_state["error"] = str(e)
        latest_state["machine_status"] = "OFFLINE"
        
    return latest_state

def send_gcode_command(cmd: str) -> str:
    """Sends a single G-code / Flashforge command to printer TCP port"""
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(2.5)
        s.connect((PRINTER_IP, PRINTER_PORT))
        
        # Gain control session first
        s.sendall(b"~M601 S1\r\n")
        time.sleep(0.05)
        s.recv(1024)
        
        formatted_cmd = cmd.strip()
        if not formatted_cmd.startswith("~"):
            formatted_cmd = "~" + formatted_cmd
        if not formatted_cmd.endswith("\r\n"):
            formatted_cmd += "\r\n"
            
        s.sendall(formatted_cmd.encode("ascii"))
        time.sleep(0.08)
        resp = s.recv(2048).decode("latin1", errors="ignore")
        s.close()
        return resp.strip()
    except Exception as e:
        return f"Error: {e}"

async def printer_poll_loop():
    while True:
        try:
            state = await asyncio.to_thread(query_printer_sync, PRINTER_IP, PRINTER_PORT)
            # Broadcast to connected websockets
            if connected_websockets:
                dead_sockets = []
                for ws in connected_websockets:
                    try:
                        await ws.send_json(state)
                    except Exception:
                        dead_sockets.append(ws)
                for ws in dead_sockets:
                    if ws in connected_websockets:
                        connected_websockets.remove(ws)
        except Exception as e:
            print("Poll loop error:", e)
            
        await asyncio.sleep(POLL_INTERVAL)

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup: Launch background poller
    poll_task = asyncio.create_task(printer_poll_loop())
    yield
    # Shutdown
    poll_task.cancel()

app = FastAPI(title="Flashforge 5M Pro Monitor", lifespan=lifespan)
templates = Jinja2Templates(directory="templates" if os.path.exists("templates") else "app/templates")

@app.get("/", response_class=HTMLResponse)
async def get_dashboard(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="index.html",
        context={
            "printer_ip": PRINTER_IP,
            "camera_url": "/api/camera/stream"
        }
    )

@app.get("/api/status")
async def get_status():
    return latest_state

@app.post("/api/control/led")
async def toggle_led():
    # Toggle LED
    current = latest_state.get("led_on", False)
    target_cmd = "~M652" if current else "~M651" # M651 is on, M652 is off in Flashforge
    resp = await asyncio.to_thread(send_gcode_command, target_cmd)
    # Refresh status immediately
    await asyncio.to_thread(query_printer_sync, PRINTER_IP, PRINTER_PORT)
    return {"status": "ok", "response": resp, "led_on": not current}

@app.post("/api/control/pause")
async def pause_print():
    resp = await asyncio.to_thread(send_gcode_command, "~M25")
    return {"status": "ok", "response": resp}

@app.post("/api/control/resume")
async def resume_print():
    resp = await asyncio.to_thread(send_gcode_command, "~M24")
    return {"status": "ok", "response": resp}

@app.get("/api/camera/stream")
async def camera_stream():
    """Proxies the MJPEG stream from the Flashforge camera"""
    async def stream_generator():
        try:
            async with httpx.AsyncClient(timeout=None) as client:
                async with client.stream("GET", CAMERA_URL) as r:
                    async for chunk in r.aiter_raw():
                        yield chunk
        except Exception as e:
            print("Camera stream proxy error:", e)

    return StreamingResponse(
        stream_generator(),
        media_type="multipart/x-mixed-replace;boundary=boundarydonotcross"
    )

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    connected_websockets.append(websocket)
    # Send immediate state on connect
    try:
        await websocket.send_json(latest_state)
        while True:
            # Keep connection alive; can receive ping/command if needed
            await websocket.receive_text()
    except WebSocketDisconnect:
        if websocket in connected_websockets:
            connected_websockets.remove(websocket)
    except Exception:
        if websocket in connected_websockets:
            connected_websockets.remove(websocket)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=4000, reload=False)
