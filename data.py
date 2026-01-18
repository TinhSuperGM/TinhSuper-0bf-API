import json, os, secrets

BASE = os.path.dirname(__file__)
API_KEYS = os.path.join(BASE, "../api/keys.json")
API_SCRIPTS = os.path.join(BASE, "../api/scripts.json")

def load(p):
    with open(p, "r", encoding="utf-8") as f:
        return json.load(f)

def save(p, d):
    with open(p, "w", encoding="utf-8") as f:
        json.dump(d, f, indent=2)

def new_script(code: str):
    sid = secrets.token_hex(6)
    data = load(API_SCRIPTS)
    data[sid] = {
        "owner": "TinhSuper",
        "code": code
    }
    save(API_SCRIPTS, data)
    return sid

def new_run_key(script_id):
    rk = "Run_" + secrets.token_hex(10)
    keys = load(API_KEYS)
    keys["run_keys"][rk] = {
        "script_id": script_id,
        "max_runs": 999999,
        "used": 0,
        "expired": False
    }
    save(API_KEYS, keys)
    return rk
