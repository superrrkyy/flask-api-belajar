"""
Unit test untuk flask-api-belajar (REST API + autentikasi API key + SQLite).

Jalankan:
    pip install -r requirements.txt -r requirements-dev.txt
    pytest -q
"""
import importlib
import json
import os
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))


@pytest.fixture(scope="module")
def api(tmp_path_factory):
    """Impor api.py dengan file key & DB terpisah (tidak menyentuh data asli)."""
    data_dir = tmp_path_factory.mktemp("data")
    os.environ["KEY_FILE"] = str(data_dir / "api_key.json")
    os.environ["DB_FILE"] = str(data_dir / "data.db")

    module = importlib.import_module("api")
    importlib.reload(module)  # pastikan env di atas dipakai
    module.app.config.update(TESTING=True)
    return module


@pytest.fixture()
def client(api):
    with api.app.test_client() as c:
        yield c


@pytest.fixture()
def key(api):
    return next(iter(api.VALID_KEYS))


def auth(key):
    return {"X-API-Key": key}


# =========================
# API KEY
# =========================
def test_file_key_dibuat_dan_berisi_hex_32_karakter(api):
    path = Path(api.KEY_FILE)
    assert path.exists(), "file API key harus dibuat otomatis"
    keys = json.loads(path.read_text())
    assert len(keys) == 1
    (k,) = keys.keys()
    assert len(k) == 32
    int(k, 16)  # harus hex yang valid


def test_endpoint_terbuka_untuk_semua(client):
    res = client.get("/")
    assert res.status_code == 200
    assert "Selamat datang" in res.get_json()["message"]


# =========================
# AUTENTIKASI
# =========================
def test_tanpa_api_key_ditolak(client):
    res = client.get("/data")
    assert res.status_code == 401
    assert res.get_json()["error"] == "API key tidak valid"


def test_api_key_salah_ditolak(client):
    res = client.get("/data", headers=auth("kunci-palsu"))
    assert res.status_code == 401


def test_api_key_benar_diterima(client, key):
    res = client.get("/data", headers=auth(key))
    assert res.status_code == 200
    assert "rahasia" in res.get_json()["data"]


def test_semua_endpoint_items_butuh_api_key(client):
    for method, url in [
        ("get", "/items"),
        ("get", "/items/1"),
        ("post", "/items"),
        ("put", "/items/1"),
        ("delete", "/items/1"),
    ]:
        res = getattr(client, method)(url)
        assert res.status_code == 401, f"{method.upper()} {url} seharusnya 401"


# =========================
# CRUD
# =========================
def test_alur_crud_lengkap(client, key):
    h = auth(key)

    # daftar awal (mungkin kosong)
    res = client.get("/items", headers=h)
    assert res.status_code == 200
    assert isinstance(res.get_json()["items"], list)

    # tambah
    res = client.post("/items", json={"item": "Belajar Flask"}, headers=h)
    assert res.status_code == 201
    item_id = res.get_json()["item"]["id"]

    # baca satu
    res = client.get(f"/items/{item_id}", headers=h)
    assert res.status_code == 200
    assert res.get_json()["item"] == "Belajar Flask"

    # ada di daftar
    res = client.get("/items", headers=h)
    assert any(i["id"] == item_id for i in res.get_json()["items"])

    # ubah
    res = client.put(f"/items/{item_id}", json={"item": "Belajar Flask + SQLite"}, headers=h)
    assert res.status_code == 200
    res = client.get(f"/items/{item_id}", headers=h)
    assert res.get_json()["item"] == "Belajar Flask + SQLite"

    # hapus
    res = client.delete(f"/items/{item_id}", headers=h)
    assert res.status_code == 200
    res = client.get(f"/items/{item_id}", headers=h)
    assert res.status_code == 404


@pytest.mark.parametrize(
    "payload",
    [
        {},
        {"item": ""},
        {"item": "   "},
        {"item": 123},
        {"item": None},
    ],
)
def test_post_item_tidak_valid_ditolak(client, key, payload):
    res = client.post("/items", json=payload, headers=auth(key))
    assert res.status_code == 400


def test_put_item_tidak_ada_404(client, key):
    res = client.put("/items/999999", json={"item": "X"}, headers=auth(key))
    assert res.status_code == 404


def test_delete_item_tidak_ada_404(client, key):
    res = client.delete("/items/999999", headers=auth(key))
    assert res.status_code == 404


def test_item_disimpan_secara_aman_dari_sql_injection(client, key):
    """Nilai jahat harus tersimpan apa adanya sebagai teks, bukan dieksekusi."""
    jahat = "'); DROP TABLE items;--"
    res = client.post("/items", json={"item": jahat}, headers=auth(key))
    assert res.status_code == 201
    item_id = res.get_json()["item"]["id"]

    res = client.get(f"/items/{item_id}", headers=auth(key))
    assert res.get_json()["item"] == jahat

    # tabel masih ada
    res = client.get("/items", headers=auth(key))
    assert res.status_code == 200


# =========================
# ERROR HANDLER
# =========================
def test_endpoint_tidak_dikenal_balas_json_404(client):
    res = client.get("/tidak-ada-endpoint-ini")
    assert res.status_code == 404
    assert "Endpoint tidak ditemukan" in res.get_json()["error"]


def test_method_salah_balas_json_405(client):
    res = client.delete("/")
    assert res.status_code == 405
    assert "Method tidak diizinkan" in res.get_json()["error"]
