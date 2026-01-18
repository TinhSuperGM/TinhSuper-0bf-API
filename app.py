from fastapi import FastAPI, HTTPException
import json, os

BASE = os.path.dirname(__file__)
KEYS = os.path.join(BASE, "keys.json")
SCRIPTS = os.path.join(BASE, "scripts.json")

app = FastAPI()

def load_json(p):
    with open(p, "r", encoding="utf-8") as f:
        return json.load(f)

def save_json(p, d):
    with open(p, "w", encoding="utf-8") as f:
        json.dump(d, f, indent=2)

@app.get("/run")
def run_script(k: str, id: str):
    keys = load_json(KEYS)
    scripts = load_json(SCRIPTS)

    rk = keys["run_keys"].get(k)
    if not rk:
        raise HTTPException(403, "Invalid run key")

    if rk["script_id"] != id:
        raise HTTPException(403, "Script ID mismatch")

    if rk["used"] >= rk["max_runs"]:
        raise HTTPException(403, "Run limit reached")

    if id not in scripts:
        raise HTTPException(404, "Script not found")

    rk["used"] += 1
    save_json(KEYS, keys)

    return scripts[id]["code"]

@app.get("/admin/get")
def admin_get(key: str, id: str):
    keys = load_json(KEYS)
    if key != keys["premium_key"]:
        raise HTTPException(403, "Invalid premium key")

    scripts = load_json(SCRIPTS)
    if id not in scripts:
        raise HTTPException(404, "Script not found")

    return scripts[id]["code"]
