"""
flask-api-belajar
REST API sederhana dengan autentikasi API key + penyimpanan SQLite.
"""
import json
import os
import secrets
import sqlite3
from functools import wraps

from flask import Flask, g, jsonify, request

app = Flask(__name__)

KEY_FILE = os.getenv("KEY_FILE", "api_key.json")
DB_FILE = os.getenv("DB_FILE", "data.db")


# =========================
# API KEY
# =========================
def load_keys():
    """Muat API key dari file, atau buat baru jika belum ada."""
    if os.path.exists(KEY_FILE):
        with open(KEY_FILE) as f:
            return json.load(f)

    new_key = secrets.token_hex(16)
    keys = {new_key: "user_pertama"}
    with open(KEY_FILE, "w") as f:
        json.dump(keys, f, indent=2)
    print(f"🔑 API key baru dibuat dan disimpan di {KEY_FILE}")
    return keys


VALID_KEYS = load_keys()


def require_api_key(func):
    """Decorator: tolak request tanpa API key yang valid."""
    @wraps(func)
    def wrapper(*args, **kwargs):
        key = request.headers.get("X-API-Key", "")
        if not any(secrets.compare_digest(key, k) for k in VALID_KEYS):
            return jsonify({"error": "API key tidak valid"}), 401
        return func(*args, **kwargs)
    return wrapper


# =========================
# DATABASE
# =========================
def get_db():
    if "db" not in g:
        g.db = sqlite3.connect(DB_FILE)
        g.db.row_factory = sqlite3.Row
    return g.db


@app.teardown_appcontext
def close_db(_exc):
    db = g.pop("db", None)
    if db is not None:
        db.close()


def init_db():
    with sqlite3.connect(DB_FILE) as db:
        db.execute(
            "CREATE TABLE IF NOT EXISTS items ("
            " id INTEGER PRIMARY KEY AUTOINCREMENT,"
            " item TEXT NOT NULL)"
        )


init_db()


def get_item_text():
    """Ambil field 'item' dari body JSON dengan aman."""
    body = request.get_json(silent=True) or {}
    item = body.get("item")
    if not isinstance(item, str) or not item.strip():
        return None
    return item.strip()


# =========================
# ROUTES
# =========================
@app.get("/")
def home():
    return jsonify({"message": "Selamat datang di API buatanmu!"})


@app.get("/data")
@require_api_key
def data():
    return jsonify({"data": "Ini data rahasia, kamu berhasil akses!"})


@app.get("/items")
@require_api_key
def get_items():
    rows = get_db().execute("SELECT id, item FROM items").fetchall()
    return jsonify({"items": [dict(r) for r in rows]})


@app.get("/items/<int:item_id>")
@require_api_key
def get_item(item_id):
    row = get_db().execute(
        "SELECT id, item FROM items WHERE id = ?", (item_id,)
    ).fetchone()
    if row is None:
        return jsonify({"error": "Item tidak ditemukan"}), 404
    return jsonify(dict(row))


@app.post("/items")
@require_api_key
def add_item():
    item = get_item_text()
    if item is None:
        return jsonify({"error": "Field 'item' wajib diisi (teks)"}), 400
    db = get_db()
    cur = db.execute("INSERT INTO items (item) VALUES (?)", (item,))
    db.commit()
    return jsonify({"message": "Item ditambahkan",
                    "item": {"id": cur.lastrowid, "item": item}}), 201


@app.put("/items/<int:item_id>")
@require_api_key
def update_item(item_id):
    item = get_item_text()
    if item is None:
        return jsonify({"error": "Field 'item' wajib diisi (teks)"}), 400
    db = get_db()
    cur = db.execute("UPDATE items SET item = ? WHERE id = ?", (item, item_id))
    db.commit()
    if cur.rowcount == 0:
        return jsonify({"error": "Item tidak ditemukan"}), 404
    return jsonify({"message": "Item diperbarui",
                    "item": {"id": item_id, "item": item}})


@app.delete("/items/<int:item_id>")
@require_api_key
def delete_item(item_id):
    db = get_db()
    cur = db.execute("DELETE FROM items WHERE id = ?", (item_id,))
    db.commit()
    if cur.rowcount == 0:
        return jsonify({"error": "Item tidak ditemukan"}), 404
    return jsonify({"message": "Item dihapus"})


@app.errorhandler(404)
def not_found(_e):
    return jsonify({"error": "Endpoint tidak ditemukan"}), 404


@app.errorhandler(405)
def method_not_allowed(_e):
    return jsonify({"error": "Method tidak diizinkan"}), 405


if __name__ == "__main__":
    debug = os.getenv("FLASK_DEBUG", "0") == "1"
    app.run(host="0.0.0.0", port=int(os.getenv("PORT", 5000)), debug=debug)
