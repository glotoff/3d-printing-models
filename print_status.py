#!/usr/bin/env python3
"""
Flashforge Adventurer 5M Pro - Command-line Print Progress Monitor
Usage:
    python print_status.py          # Quick one-off status snapshot
    python print_status.py --watch  # Live auto-refreshing monitor (every 5s)
"""

import socket
import re
import sys
import time
import argparse

# Ensure standard output can print Unicode / UTF-8 on Windows
if hasattr(sys.stdout, "reconfigure"):
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass

PRINTER_IP = "192.168.50.99"
PRINTER_PORT = 8899

def query_printer(ip=PRINTER_IP, port=PRINTER_PORT, timeout=3.0):
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(timeout)
        s.connect((ip, port))
        
        cmds = ["~M119\r\n", "~M105\r\n", "~M27\r\n"]
        responses = {}
        
        for cmd in cmds:
            s.sendall(cmd.encode("ascii"))
            time.sleep(0.06)
            data = s.recv(1024).decode("latin1", errors="ignore")
            responses[cmd.strip()] = data
            
        s.close()
        return parse_status(responses)
    except socket.timeout:
        return {"error": f"Connection to {ip}:{port} timed out"}
    except ConnectionRefusedError:
        return {"error": f"Connection refused by {ip}:{port}"}
    except Exception as e:
        return {"error": str(e)}

def parse_status(raw):
    status = {
        "connected": True,
        "machine_status": "IDLE",
        "current_file": "None",
        "nozzle_temp": 0.0,
        "nozzle_target": 0.0,
        "bed_temp": 0.0,
        "bed_target": 0.0,
        "progress_pct": 0,
        "current_layer": 0,
        "total_layers": 0
    }
    
    # Parse ~M119
    m119 = raw.get("~M119", "")
    m_stat = re.search(r"MachineStatus:\s*([A-Za-z0-9_]+)", m119)
    if m_stat:
        status["machine_status"] = m_stat.group(1)
        
    m_file = re.search(r"CurrentFile:\s*(.+)", m119)
    if m_file:
        status["current_file"] = m_file.group(1).strip()
        
    # Parse ~M105 (T0:220.5/220.0 B:50.0/50.0)
    m105 = raw.get("~M105", "")
    m_nozzle = re.search(r"T0:([\d\.]+)/([\d\.]+)", m105)
    if m_nozzle:
        status["nozzle_temp"] = float(m_nozzle.group(1))
        status["nozzle_target"] = float(m_nozzle.group(2))
        
    m_bed = re.search(r"B:([\d\.]+)/([\d\.]+)", m105)
    if m_bed:
        status["bed_temp"] = float(m_bed.group(1))
        status["bed_target"] = float(m_bed.group(2))
        
    # Parse ~M27
    m27 = raw.get("~M27", "")
    m_pct = re.search(r"SD printing byte (\d+)/100", m27)
    if m_pct:
        status["progress_pct"] = int(m_pct.group(1))
        
    m_layer = re.search(r"Layer:\s*(\d+)/(\d+)", m27)
    if m_layer:
        status["current_layer"] = int(m_layer.group(1))
        status["total_layers"] = int(m_layer.group(2))
        if status["total_layers"] > 0:
            layer_pct = int(round((status["current_layer"] / status["total_layers"]) * 100))
            if layer_pct > status["progress_pct"]:
                status["progress_pct"] = layer_pct
                
    return status

def format_bar(pct, width=28):
    filled = int(round(width * (pct / 100.0)))
    empty = width - filled
    return "=" * filled + "-" * empty

def render_display(st):
    if "error" in st:
        return f"\n  [!] Printer Error: {st['error']}\n"
    
    status_tag = "PRINTING" if "BUILDING" in st["machine_status"] else st["machine_status"]
    bar = format_bar(st["progress_pct"])
    
    out = []
    out.append("+" + "-" * 56 + "+")
    out.append(f"|  Flashforge Adventurer 5M Pro  [{status_tag:^14}]    |")
    out.append("+" + "-" * 56 + "+")
    out.append(f"|  File:     {st['current_file']:<43} |")
    out.append(f"|  Progress: [{bar}] {st['progress_pct']:>3}%      |")
    
    if st["total_layers"] > 0:
        layer_str = f"Layer {st['current_layer']} of {st['total_layers']}"
        out.append(f"|  Layers:   {layer_str:<43} |")
        
    temp_str = f"Nozzle: {st['nozzle_temp']}C / {st['nozzle_target']}C  |  Bed: {st['bed_temp']}C / {st['bed_target']}C"
    out.append(f"|  Temps:    {temp_str:<43} |")
    out.append("+" + "-" * 56 + "+")
    return "\n".join(out)

def main():
    parser = argparse.ArgumentParser(description="Flashforge Print Status Monitor")
    parser.add_argument("--watch", "-w", action="store_true", help="Monitor live in terminal (refreshes every 5s)")
    parser.add_argument("--interval", "-i", type=int, default=5, help="Refresh interval in seconds (default: 5)")
    args = parser.parse_args()

    if args.watch:
        print("\nStarting live print monitor (Press Ctrl+C to stop)...\n")
        try:
            while True:
                st = query_printer()
                sys.stdout.write("\033[H\033[J")
                print(render_display(st))
                time.sleep(args.interval)
        except KeyboardInterrupt:
            print("\nStopped.")
    else:
        st = query_printer()
        print(render_display(st))

if __name__ == "__main__":
    main()
