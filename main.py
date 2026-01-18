from fastapi import FastAPI, Header, HTTPException
import json, uuid

app = FastAPI()

def load_json(name):
    with open(name, "r", encoding="utf-8") as f:
        return json.load(f)

def save_json(name, data):
    with open(name, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)

@app.post("/create")
def create_script(data: dict, authorization: str = Header(None)):
    keys = load_json("keys.json")
    if authorization != keys["premium"]:
        raise HTTPException(status_code=403, detail="Invalid Premium Key")

    script_id = uuid.uuid4().hex[:12]
    scripts = load_json("scripts.json")
    scripts[script_id] = {
        "code": data["code"]
    }
    save_json("scripts.json", scripts)

    run_key = "Run_" + uuid.uuid4().hex[:19]
    keys["run_keys"][run_key] = script_id
    save_json("keys.json", keys)

    return {
        "id": script_id,
        "run_key": run_key
    }

@app.get("/run/{script_id}")
def run_script(script_id: str, key: str):
    keys = load_json("keys.json")
    if key not in keys["run_keys"]:
        raise HTTPException(status_code=403, detail="Invalid Run Key")
    if keys["run_keys"][key] != script_id:
        raise HTTPException(status_code=403, detail="Key not match script")

    scripts = load_json("scripts.json")
    return scripts[script_id]["code"]

@app.post("/premium/deobf")
def premium_deobf(data: dict, authorization: str = Header(None)):
    keys = load_json("keys.json")
    if authorization != keys["premium"]:
        raise HTTPException(status_code=403)

    scripts = load_json("scripts.json")
    return scripts.get(data["id"])
