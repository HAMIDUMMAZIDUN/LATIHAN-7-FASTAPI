from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional
import sqlite3
import os
from datetime import datetime

# Inisialisasi FastAPI
app = FastAPI(
    title="FastAPI CRUD Application",
    description="API sederhana untuk tambah dan tampil daftar data",
    version="1.0.0"
)

# Konfigurasi CORS untuk aplikasi Android
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Dalam production, ganti dengan domain spesifik
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Database setup
DATABASE_URL = "data.db"

def init_db():
    """Inisialisasi database dan tabel"""
    conn = sqlite3.connect(DATABASE_URL)
    cursor = conn.cursor()
    
    # Membuat tabel items jika belum ada
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS items (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nama TEXT NOT NULL,
            deskripsi TEXT,
            harga REAL,
            kategori TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
    
    conn.commit()
    conn.close()

# Model Pydantic untuk request/response
class ItemCreate(BaseModel):
    nama: str
    deskripsi: Optional[str] = None
    harga: Optional[float] = None
    kategori: Optional[str] = None

class ItemUpdate(BaseModel):
    nama: Optional[str] = None
    deskripsi: Optional[str] = None
    harga: Optional[float] = None
    kategori: Optional[str] = None

class ItemResponse(BaseModel):
    id: int
    nama: str
    deskripsi: Optional[str]
    harga: Optional[float]
    kategori: Optional[str]
    created_at: str
    updated_at: str

# Inisialisasi database saat startup
@app.on_event("startup")
async def startup_event():
    init_db()

# Root endpoint
@app.get("/")
async def root():
    return {
        "message": "Selamat datang di FastAPI CRUD Application",
        "docs": "/docs",
        "endpoints": {
            "GET /items": "Tampil semua data",
            "GET /items/{id}": "Tampil data berdasarkan ID",
            "POST /items": "Tambah data baru",
            "PUT /items/{id}": "Update data",
            "DELETE /items/{id}": "Hapus data"
        }
    }

# GET - Tampil semua data
@app.get("/items", response_model=List[ItemResponse])
async def get_all_items():
    """Mengambil semua data items"""
    conn = sqlite3.connect(DATABASE_URL)
    conn.row_factory = sqlite3.Row  # Untuk akses kolom by name
    cursor = conn.cursor()
    
    cursor.execute("SELECT * FROM items ORDER BY created_at DESC")
    rows = cursor.fetchall()
    conn.close()
    
    items = []
    for row in rows:
        items.append({
            "id": row["id"],
            "nama": row["nama"],
            "deskripsi": row["deskripsi"],
            "harga": row["harga"],
            "kategori": row["kategori"],
            "created_at": row["created_at"],
            "updated_at": row["updated_at"]
        })
    
    return items

# GET - Tampil data berdasarkan ID
@app.get("/items/{item_id}", response_model=ItemResponse)
async def get_item(item_id: int):
    """Mengambil data item berdasarkan ID"""
    conn = sqlite3.connect(DATABASE_URL)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    
    cursor.execute("SELECT * FROM items WHERE id = ?", (item_id,))
    row = cursor.fetchone()
    conn.close()
    
    if not row:
        raise HTTPException(status_code=404, detail="Item tidak ditemukan")
    
    return {
        "id": row["id"],
        "nama": row["nama"],
        "deskripsi": row["deskripsi"],
        "harga": row["harga"],
        "kategori": row["kategori"],
        "created_at": row["created_at"],
        "updated_at": row["updated_at"]
    }

# POST - Tambah data baru
@app.post("/items", response_model=ItemResponse)
async def create_item(item: ItemCreate):
    """Menambah data item baru"""
    conn = sqlite3.connect(DATABASE_URL)
    cursor = conn.cursor()
    
    cursor.execute("""
        INSERT INTO items (nama, deskripsi, harga, kategori)
        VALUES (?, ?, ?, ?)
    """, (item.nama, item.deskripsi, item.harga, item.kategori))
    
    item_id = cursor.lastrowid
    conn.commit()
    
    # Ambil data yang baru dibuat
    cursor.execute("SELECT * FROM items WHERE id = ?", (item_id,))
    conn.row_factory = sqlite3.Row
    row = cursor.fetchone()
    conn.close()
    
    return {
        "id": row["id"],
        "nama": row["nama"],
        "deskripsi": row["deskripsi"],
        "harga": row["harga"],
        "kategori": row["kategori"],
        "created_at": row["created_at"],
        "updated_at": row["updated_at"]
    }

# PUT - Update data
@app.put("/items/{item_id}", response_model=ItemResponse)
async def update_item(item_id: int, item: ItemUpdate):
    """Update data item berdasarkan ID"""
    conn = sqlite3.connect(DATABASE_URL)
    cursor = conn.cursor()
    
    # Cek apakah item ada
    cursor.execute("SELECT id FROM items WHERE id = ?", (item_id,))
    if not cursor.fetchone():
        conn.close()
        raise HTTPException(status_code=404, detail="Item tidak ditemukan")
    
    # Update hanya field yang diberikan
    update_fields = []
    values = []
    
    if item.nama is not None:
        update_fields.append("nama = ?")
        values.append(item.nama)
    if item.deskripsi is not None:
        update_fields.append("deskripsi = ?")
        values.append(item.deskripsi)
    if item.harga is not None:
        update_fields.append("harga = ?")
        values.append(item.harga)
    if item.kategori is not None:
        update_fields.append("kategori = ?")
        values.append(item.kategori)
    
    if not update_fields:
        conn.close()
        raise HTTPException(status_code=400, detail="Tidak ada field yang diupdate")
    
    update_fields.append("updated_at = CURRENT_TIMESTAMP")
    values.append(item_id)
    
    query = f"UPDATE items SET {', '.join(update_fields)} WHERE id = ?"
    cursor.execute(query, values)
    conn.commit()
    
    # Ambil data yang sudah diupdate
    conn.row_factory = sqlite3.Row
    cursor.execute("SELECT * FROM items WHERE id = ?", (item_id,))
    row = cursor.fetchone()
    conn.close()
    
    return {
        "id": row["id"],
        "nama": row["nama"],
        "deskripsi": row["deskripsi"],
        "harga": row["harga"],
        "kategori": row["kategori"],
        "created_at": row["created_at"],
        "updated_at": row["updated_at"]
    }

# DELETE - Hapus data
@app.delete("/items/{item_id}")
async def delete_item(item_id: int):
    """Hapus data item berdasarkan ID"""
    conn = sqlite3.connect(DATABASE_URL)
    cursor = conn.cursor()
    
    # Cek apakah item ada
    cursor.execute("SELECT id FROM items WHERE id = ?", (item_id,))
    if not cursor.fetchone():
        conn.close()
        raise HTTPException(status_code=404, detail="Item tidak ditemukan")
    
    # Hapus item
    cursor.execute("DELETE FROM items WHERE id = ?", (item_id,))
    conn.commit()
    conn.close()
    
    return {"message": f"Item dengan ID {item_id} berhasil dihapus"}

# GET - Statistik data
@app.get("/stats")
async def get_stats():
    """Mengambil statistik data"""
    conn = sqlite3.connect(DATABASE_URL)
    cursor = conn.cursor()
    
    # Total items
    cursor.execute("SELECT COUNT(*) as total FROM items")
    total = cursor.fetchone()[0]
    
    # Items berdasarkan kategori
    cursor.execute("""
        SELECT kategori, COUNT(*) as count 
        FROM items 
        WHERE kategori IS NOT NULL 
        GROUP BY kategori
    """)
    categories = cursor.fetchall()
    
    conn.close()
    
    return {
        "total_items": total,
        "categories": [{"kategori": cat[0], "count": cat[1]} for cat in categories]
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000) 