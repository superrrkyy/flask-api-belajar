<p align="center">
  <img src="./assets/banner.svg" width="100%" alt="Flask API" />
</p>

<p align="center">
  <img src="https://readme-typing-svg.demolab.com?font=Fira+Code&weight=600&size=16&duration=2800&pause=700&color=FACC15&center=true&vCenter=true&width=340&height=30&lines=Belajar+REST+API+%F0%9F%90%8D;Autentikasi+API+Key+%F0%9F%94%91;CRUD+%2B+SQLite+%F0%9F%92%BE" alt="typing" />
</p>

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.9+-3776AB?style=flat-square&logo=python&logoColor=white" />
  <img src="https://img.shields.io/badge/Flask-3.x-000000?style=flat-square&logo=flask&logoColor=white" />
  <img src="https://img.shields.io/badge/SQLite-built--in-003B57?style=flat-square&logo=sqlite&logoColor=white" />
  <img src="https://img.shields.io/badge/license-MIT-7c3aed?style=flat-square" />
</p>

<p align="center">
  <a href="#-instalasi"><b>Instalasi</b></a> •
  <a href="#-endpoint"><b>Endpoint</b></a> •
  <a href="#-contoh-request"><b>Contoh</b></a> •
  <a href="#-cara-kerja"><b>Cara Kerja</b></a>
</p>

---

### ✨ Fitur

- 🔑 **API key otomatis**: dibuat sekali saat pertama kali dijalankan
- 🛡️ **Decorator `@require_api_key`**: proteksi endpoint cukup dengan 1 baris
- 📦 **CRUD lengkap**: tambah, lihat, ubah, hapus item
- 💾 **SQLite**: data tidak hilang saat server restart
- ✅ **Validasi input**: body yang bukan JSON tidak membuat server error
- 🧾 **Respons JSON konsisten**, termasuk untuk error 404 dan 405

---

### 🚀 Instalasi

```bash
git clone https://github.com/superrrkyy/flask-api-belajar.git
cd flask-api-belajar
pip install -r requirements.txt
python api.py
```

Server berjalan di `http://localhost:5000` 🎉

> [!IMPORTANT]
> Saat pertama dijalankan, API key dibuat otomatis dan disimpan di **`api_key.json`**. Buka file itu untuk melihat key-mu.
> File ini sudah masuk `.gitignore`, jadi **jangan pernah meng-upload-nya ke GitHub**.

<details>
<summary><b>📱 Menjalankan di Termux (ketuk untuk membuka)</b></summary>
<br>

```bash
pkg install python git -y
git clone https://github.com/superrrkyy/flask-api-belajar.git
cd flask-api-belajar
pip install -r requirements.txt
python api.py
cat api_key.json   # lihat API key
```

</details>

---

### 📡 Endpoint

Semua endpoint bertanda 🔒 membutuhkan header `X-API-Key`.

| Method | Endpoint | Auth | Fungsi |
|:--|:--|:-:|:--|
| `GET` | `/` | – | Pesan sambutan |
| `GET` | `/data` | 🔒 | Contoh data rahasia |
| `GET` | `/items` | 🔒 | Lihat semua item |
| `GET` | `/items/<id>` | 🔒 | Lihat 1 item |
| `POST` | `/items` | 🔒 | Tambah item |
| `PUT` | `/items/<id>` | 🔒 | Ubah item |
| `DELETE` | `/items/<id>` | 🔒 | Hapus item |

---

### 🧪 Contoh Request

```bash
KEY="api_key_kamu"

# Tambah item
curl -X POST http://localhost:5000/items \
  -H "X-API-Key: $KEY" -H "Content-Type: application/json" \
  -d '{"item": "buku"}'

# Lihat semua item
curl http://localhost:5000/items -H "X-API-Key: $KEY"

# Ubah item id 1
curl -X PUT http://localhost:5000/items/1 \
  -H "X-API-Key: $KEY" -H "Content-Type: application/json" \
  -d '{"item": "pena"}'

# Hapus item id 1
curl -X DELETE http://localhost:5000/items/1 -H "X-API-Key: $KEY"
```

<details>
<summary><b>📥 Contoh respons</b></summary>
<br>

```json
// POST /items  → 201 Created
{ "message": "Item ditambahkan", "item": { "id": 1, "item": "buku" } }

// GET /items   → 200 OK
{ "items": [ { "id": 1, "item": "buku" } ] }

// Tanpa / salah API key → 401
{ "error": "API key tidak valid" }

// Body kosong / bukan JSON → 400
{ "error": "Field 'item' wajib diisi (teks)" }
```

</details>

---

### 🧠 Cara Kerja

```python
@app.get("/items")
@require_api_key          # ← cek header X-API-Key dulu
def get_items():
    ...
```

1. Saat start, `api.py` memuat key dari `api_key.json`, atau membuat key baru jika file belum ada.
2. Decorator `@require_api_key` mengecek header `X-API-Key` di setiap request. Kalau salah, server membalas **401**.
3. Data disimpan di **`data.db`** (SQLite) yang dibuat otomatis.

---

### ⚙️ Konfigurasi (opsional)

| Variabel | Default | Keterangan |
|:--|:--|:--|
| `PORT` | `5000` | Port server |
| `FLASK_DEBUG` | `0` | Isi `1` untuk mode debug |
| `KEY_FILE` | `api_key.json` | Lokasi file API key |
| `DB_FILE` | `data.db` | Lokasi database |

---

### 🗺️ Rencana Pengembangan

- [ ] Endpoint untuk membuat & mencabut API key
- [ ] Rate limiting
- [ ] Dokumentasi Swagger / OpenAPI
- [ ] Deploy ke cloud

---

<p align="center">
  Dibuat dengan 💜 oleh <a href="https://github.com/superrrkyy"><b>AXRYZURE</b></a> • Lisensi <a href="LICENSE">MIT</a>
  <br><br>
  <sub>⭐ Beri bintang jika repo ini membantumu belajar!</sub>
</p>
