from flask import Flask, request, jsonify
import secrets
import json
import os

app = Flask(__name__)
KEY_FILE = "api_key.json"

# Load atau bikin API key permanen
if os.path.exists(KEY_FILE):
    with open(KEY_FILE) as f:
        VALID_KEYS = json.load(f)
else:
    new_key = secrets.token_hex(16)
    VALID_KEYS = {new_key: "user_pertama"}
    with open(KEY_FILE, "w") as f:
        json.dump(VALID_KEYS, f)

print("API Key kamu:", list(VALID_KEYS.keys())[0])

# Simpan data sederhana di memori
items = []

def cek_api_key():
    key = request.headers.get("X-API-Key")
    return key in VALID_KEYS

@app.route("/")
def home():
    return jsonify({"message": "Selamat datang di API buatanmu!"})

@app.route("/data")
def data():
    if not cek_api_key():
        return jsonify({"error": "API key tidak valid"}), 401
    return jsonify({"data": "Ini data rahasia, kamu berhasil akses!"})

@app.route("/items", methods=["GET"])
def get_items():
    if not cek_api_key():
        return jsonify({"error": "API key tidak valid"}), 401
    return jsonify({"items": items})

@app.route("/items", methods=["POST"])
def add_item():
    if not cek_api_key():
        return jsonify({"error": "API key tidak valid"}), 401
    new_item = request.json.get("item")
    if not new_item:
        return jsonify({"error": "Field 'item' wajib diisi"}), 400
    items.append(new_item)
    return jsonify({"message": "Item ditambahkan", "items": items}), 201

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
