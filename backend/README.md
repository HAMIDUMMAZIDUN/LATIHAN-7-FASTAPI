# FastAPI CRUD Application

API sederhana menggunakan FastAPI untuk operasi CRUD (Create, Read, Update, Delete) dengan database SQLite.

## 🚀 Fitur

- ✅ **CREATE**: Tambah data baru
- ✅ **READ**: Tampil semua data dan data berdasarkan ID
- ✅ **UPDATE**: Update data berdasarkan ID
- ✅ **DELETE**: Hapus data berdasarkan ID
- ✅ **STATS**: Statistik data
- ✅ **CORS**: Configured untuk aplikasi Android
- ✅ **Database**: SQLite untuk penyimpanan data
- ✅ **Dokumentasi**: Auto-generated dengan Swagger UI

## 📋 Prerequisite

- Python 3.8 atau lebih tinggi
- pip (Python package manager)

## 🛠️ Instalasi

1. **Clone atau download proyek ini**

2. **Masuk ke folder backend**

   ```bash
   cd backend
   ```

3. **Buat virtual environment (opsional tapi direkomendasikan)**

   ```bash
   python -m venv venv

   # Windows
   venv\Scripts\activate

   # Linux/Mac
   source venv/bin/activate
   ```

4. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

## 🏃‍♂️ Menjalankan Server

### Opsi 1: Menggunakan run.py (Direkomendasikan)

```bash
python run.py
```

### Opsi 2: Menggunakan uvicorn langsung

```bash
uvicorn main:app --host 0.0.0.0 --port 8000 --reload
```

Server akan berjalan di:

- **API**: http://localhost:8000
- **Dokumentasi**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

## 📡 Endpoint API

### Base URL

```
http://localhost:8000
```

### Endpoints

| Method | Endpoint      | Deskripsi                 |
| ------ | ------------- | ------------------------- |
| GET    | `/`           | Info API                  |
| GET    | `/items`      | Ambil semua data          |
| GET    | `/items/{id}` | Ambil data berdasarkan ID |
| POST   | `/items`      | Tambah data baru          |
| PUT    | `/items/{id}` | Update data               |
| DELETE | `/items/{id}` | Hapus data                |
| GET    | `/stats`      | Statistik data            |

### Contoh Request

#### 1. Tambah Data Baru (POST)

```bash
curl -X POST "http://localhost:8000/items" \
     -H "Content-Type: application/json" \
     -d '{
       "nama": "Laptop Gaming",
       "deskripsi": "Laptop untuk gaming dengan spek tinggi",
       "harga": 15000000,
       "kategori": "Elektronik"
     }'
```

#### 2. Ambil Semua Data (GET)

```bash
curl -X GET "http://localhost:8000/items"
```

#### 3. Ambil Data Berdasarkan ID (GET)

```bash
curl -X GET "http://localhost:8000/items/1"
```

#### 4. Update Data (PUT)

```bash
curl -X PUT "http://localhost:8000/items/1" \
     -H "Content-Type: application/json" \
     -d '{
       "nama": "Laptop Gaming Updated",
       "harga": 14000000
     }'
```

#### 5. Hapus Data (DELETE)

```bash
curl -X DELETE "http://localhost:8000/items/1"
```

## 📊 Model Data

### ItemCreate (untuk POST)

```json
{
  "nama": "string (required)",
  "deskripsi": "string (optional)",
  "harga": "number (optional)",
  "kategori": "string (optional)"
}
```

### ItemUpdate (untuk PUT)

```json
{
  "nama": "string (optional)",
  "deskripsi": "string (optional)",
  "harga": "number (optional)",
  "kategori": "string (optional)"
}
```

### ItemResponse (untuk GET)

```json
{
  "id": "integer",
  "nama": "string",
  "deskripsi": "string",
  "harga": "number",
  "kategori": "string",
  "created_at": "string",
  "updated_at": "string"
}
```

## 📱 Integrasi dengan Android

API ini sudah dikonfigurasi dengan CORS untuk bisa diakses dari aplikasi Android. Gunakan URL berikut dalam aplikasi Android Anda:

```kotlin
// Base URL untuk API
const val BASE_URL = "http://YOUR_IP_ADDRESS:8000/"

// Contoh untuk localhost (emulator)
const val BASE_URL = "http://10.0.2.2:8000/"

// Contoh untuk device fisik
const val BASE_URL = "http://192.168.1.100:8000/"
```

## 🗄️ Database

- Database menggunakan SQLite
- File database: `data.db` (akan dibuat otomatis)
- Tabel: `items` dengan kolom:
  - `id` (Primary Key, Auto Increment)
  - `nama` (Text, Required)
  - `deskripsi` (Text, Optional)
  - `harga` (Real, Optional)
  - `kategori` (Text, Optional)
  - `created_at` (Timestamp)
  - `updated_at` (Timestamp)

## 🐛 Troubleshooting

### Server tidak bisa diakses dari Android

1. Pastikan firewall tidak memblokir port 8000
2. Ganti `localhost` dengan IP address komputer Anda
3. Untuk emulator Android, gunakan `10.0.2.2` sebagai host

### Error saat install dependencies

```bash
pip install --upgrade pip
pip install -r requirements.txt
```

### Database error

Hapus file `data.db` dan restart server untuk reset database.

## 📝 Development

Untuk development, server akan auto-reload setiap kali ada perubahan kode (jika menggunakan `--reload` flag).

## 🤝 Kontribusi

Silakan buat issue atau pull request untuk improvement.

## 📄 Lisensi

Open source - bebas digunakan untuk keperluan apapun.
