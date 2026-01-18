from fastapi import FastAPI, Header, HTTPException
import json, uuid

app = FastAPI(title="TinhSuper-0bf-API")

def load(name):
    with open(name, "r", encoding="utf-8") as f:
        return json.load(f)

def save(name, data):
    with open(name, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)

# ================= CREATE SCRIPT (BOT ONLY) =================
@app.post("/create")
def create_script(payload: dict, authorization: str = Header(None)):
    keys = load("keys.json")
    if authorization != keys["premium"]:
        raise HTTPException(403, "Invalid Premium Key")

    scripts = load("scripts.json")

    script_id = uuid.uuid4().hex[:12]
    scripts[script_id] = {
        "code": payload["code"]
    }
    save("scripts.json", scripts)

    run_key = "Run_" + uuid.uuid4().hex[:19]
    keys["run_keys"][run_key] = script_id
    save("keys.json", keys)

    return {
        "id": script_id,
        "run_key": run_key
    }

# ================= RUN SCRIPT (ROBLOX) =================
@app.get("/run/{script_id}")
def run_script(script_id: str, key: str):
    keys = load("keys.json")

    if key not in keys["run_keys"]:
        raise HTTPException(403, "Invalid Run Key")

    if keys["run_keys"][key] != script_id:
        raise HTTPException(403, "Key does not match script")

    scripts = load("scripts.json")
    if script_id not in scripts:
        raise HTTPException(404, "Script not found")

    return scripts[script_id]["code"]

# ================= DEOBF (PREMIUM) =================
@app.post("/premium/deobf")
def premium_deobf(payload: dict, authorization: str = Header(None)):
    keys = load("keys.json")
    if authorization != keys["premium"]:
        raise HTTPException(403, "Invalid Premium Key")

    scripts = load("scripts.json")
    sid = payload.get("id")

    if sid not in scripts:
        raise HTTPException(404, "Script not found")

    return scripts[sid]
