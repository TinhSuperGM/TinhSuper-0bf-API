from flask import Flask, request, jsonify
import json
import os

app = Flask(__name__)

KEYS_FILE = "keys.json"
SCRIPTS_FILE = "scripts.json"


def load_json(path):
    if not os.path.exists(path):
        return {}
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def save_json(path, data):
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4)


@app.route("/")
def home():
    return "TinhSuper OBF API running"


# ================= ADD SCRIPT (BOT ONLY) =================
@app.route("/add_script", methods=["POST"])
def add_script():
    data = request.json

    script_id = data.get("id")
    script = data.get("script")
    run_key = data.get("run_key")
    premium = data.get("premium_key")

    keys = load_json(KEYS_FILE)

    if premium != keys.get("premium_key"):
        return jsonify({"error": "Invalid premium key"}), 403

    scripts = load_json(SCRIPTS_FILE)

    scripts[script_id] = {
        "script": script,
        "run_key": run_key
    }

    keys["run_keys"][run_key] = script_id

    save_json(SCRIPTS_FILE, scripts)
    save_json(KEYS_FILE, keys)

    return jsonify({"status": "ok"})


# ================= RUN SCRIPT (ROBLOX) =================
@app.route("/run", methods=["POST"])
def run_script():
    data = request.json
    script_id = data.get("id")
    run_key = data.get("run_key")

    scripts = load_json(SCRIPTS_FILE)
    keys = load_json(KEYS_FILE)

    if run_key not in keys.get("run_keys", {}):
        return jsonify({"error": "Invalid run key"}), 403

    if keys["run_keys"][run_key] != script_id:
        return jsonify({"error": "Key not match script"}), 403

    script_data = scripts.get(script_id)
    if not script_data:
        return jsonify({"error": "Script not found"}), 404

    # ⚠️ TRẢ SCRIPT VỀ – ROBLOX SẼ loadstring
    return jsonify({
        "script": script_data["script"]
    })


# ================= PREMIUM VIEW =================
@app.route("/list", methods=["POST"])
def list_scripts():
    data = request.json
    if data.get("premium_key") != load_json(KEYS_FILE).get("premium_key"):
        return jsonify({"error": "Invalid premium key"}), 403

    return jsonify(load_json(SCRIPTS_FILE))


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
