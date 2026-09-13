import urllib.request
import json

def call_fusion_tool(tool_name, arguments):
    # 1. Initialize
    init_data = json.dumps({
        "jsonrpc": "2.0",
        "id": 1,
        "method": "initialize",
        "params": {
            "protocolVersion": "2024-11-05",
            "capabilities": {},
            "clientInfo": {"name": "antigravity", "version": "1.0"}
        }
    }).encode("utf-8")

    req = urllib.request.Request("http://127.0.0.1:27182/mcp", data=init_data, headers={"Content-Type": "application/json"})
    with urllib.request.urlopen(req) as resp:
        session_id = resp.headers.get("mcp-session-id")

    # 2. notifications/initialized
    init_notif = json.dumps({
        "jsonrpc": "2.0",
        "method": "notifications/initialized"
    }).encode("utf-8")
    req_notif = urllib.request.Request("http://127.0.0.1:27182/mcp", data=init_notif, headers={
        "Content-Type": "application/json",
        "mcp-session-id": session_id
    })
    try:
        with urllib.request.urlopen(req_notif) as resp_n:
            pass
    except: pass

    # 3. tools/call
    call_data = json.dumps({
        "jsonrpc": "2.0",
        "id": 2,
        "method": "tools/call",
        "params": {
            "name": tool_name,
            "arguments": arguments
        }
    }).encode("utf-8")

    req2 = urllib.request.Request("http://127.0.0.1:27182/mcp", data=call_data, headers={
        "Content-Type": "application/json",
        "mcp-session-id": session_id
    })
    with urllib.request.urlopen(req2) as resp2:
        res = json.loads(resp2.read().decode("utf-8"))
        return res

if __name__ == "__main__":
    test_args = {
        "featureType": "script",
        "object": {
            "readOnly": True,
            "script": "import adsk.core\ndef run(_context: str):\n    app = adsk.core.Application.get()\n    print('Fusion 360 is connected! Active doc:', app.activeDocument.name if app.activeDocument else 'None')\n"
        }
    }
    result = call_fusion_tool("fusion_mcp_execute", test_args)
    print(json.dumps(result, indent=2))
