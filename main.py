from flask import Flask, request, jsonify
import json, os, random, string, time

app = Flask(__name__)

SCRIPT_DB = "scripts.json"
KEY_DB = "keys.json"

# ================== UTILS ==================

def load_json(path):
    if not os.path.exists(path):
        return {}
    try:
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return {}

def save_json(path, data):
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)

def gen_id():
    return ''.join(random.choice(string.ascii_lowercase + string.digits) for _ in range(8))

def gen_run_key():
    return "Run_" + ''.join(random.choice(string.ascii_letters + string.digits) for _ in range(19))

def gen_noise(n=20):
    chars = string.ascii_letters + string.digits + "!@#$%^&*()_+-={}[]<>?,."
    return ''.join(random.choice(chars) for _ in range(n))

# ================== LOAD DB ==================

scripts = load_json(SCRIPT_DB)
keys = load_json(KEY_DB)
PREMIUM_KEY = keys.get("premium_key", "")

# ================== ROUTES ==================

@app.route("/")
def home():
    return "TinhSuper OBF API is running"

# ---------- ADD SCRIPT ----------
@app.route("/add", methods=["POST"])
def add_script():
    data = request.json
    if not data or "script" not in data:
        return jsonify({"error": "No script"}), 400

    sid = gen_id()
    run_key = gen_run_key()

    scripts[sid] = {
        "run_key": run_key,
        "script": data["script"],
        "created_at": int(time.time())
    }

    save_json(SCRIPT_DB, scripts)

    return jsonify({
        "id": sid,
        "run_key": run_key
    })

# ---------- RUN SCRIPT (ROBLOX) ----------
@app.route("/run", methods=["POST"])
def run_script():
    data = request.json
    if not data:
        return jsonify({"error": "No data"}), 400

    sid = data.get("id")
    run_key = data.get("run_key")

    if sid not in scripts:
        return jsonify({"error": "Invalid id"}), 403

    entry = scripts[sid]
    if entry["run_key"] != run_key:
        return jsonify({"error": "Invalid run key"}), 403

    # Roblox sẽ nhận script ở đây
    return jsonify({
        "script": entry["script"]
    })

# ---------- ADMIN GET (DEOBF) ----------
@app.route("/admin/get", methods=["POST"])
def admin_get():
    data = request.json
    if not data:
        return jsonify({"error": "No data"}), 400

    if data.get("premium_key") != PREMIUM_KEY:
        return jsonify({"error": "Unauthorized"}), 401

    sid = data.get("id")
    if sid not in scripts:
        return jsonify({"error": "Not found"}), 404

    return jsonify({
        "script": scripts[sid]["script"]
    })

# ---------- PING (RESET STORE) ----------
@app.route("/ping", methods=["GET"])
def ping():
    """
    - Keep Render alive
    - Xoá toàn bộ script cũ
    - Ghi đè bằng 1 script rác
    """
    global scripts

    noise_id = "noise"
    scripts = {
        noise_id: {
            "run_key": "noise",
            "script": gen_noise(20),
            "created_at": int(time.time())
        }
    }

    save_json(SCRIPT_DB, scripts)
    return "pong", 200

# ================== START ==================

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
