#!/usr/bin/env python3
"""
Script untuk menambahkan contoh data
Jalankan dengan: python sample_data.py
"""

import sqlite3
import json
from datetime import datetime

DATABASE_URL = "data.db"

# Contoh data
sample_items = [
    {
        "nama": "Laptop Gaming ASUS ROG",
        "deskripsi": "Laptop gaming dengan processor Intel i7, RAM 16GB, VGA RTX 3070",
        "harga": 25000000,
        "kategori": "Elektronik"
    },
    {
        "nama": "Smartphone Samsung Galaxy",
        "deskripsi": "Smartphone premium dengan kamera 108MP dan layar AMOLED",
        "harga": 12000000,
        "kategori": "Elektronik"
    },
    {
        "nama": "Sepatu Running Nike",
        "deskripsi": "Sepatu lari dengan teknologi Air Max untuk kenyamanan maksimal",
        "harga": 1500000,
        "kategori": "Olahraga"
    },
    {
        "nama": "Buku Programming Python",
        "deskripsi": "Buku panduan lengkap pemrograman Python untuk pemula hingga advanced",
        "harga": 150000,
        "kategori": "Buku"
    },
    {
        "nama": "Kopi Arabica Premium",
        "deskripsi": "Kopi arabica single origin dari dataran tinggi Jawa Barat",
        "harga": 85000,
        "kategori": "Makanan"
    },
    {
        "nama": "Headphone Sony WH-1000XM4",
        "deskripsi": "Headphone wireless dengan noise cancelling terbaik di kelasnya",
        "harga": 4500000,
        "kategori": "Audio"
    },
    {
        "nama": "Jaket Hoodie",
        "deskripsi": "Jaket hoodie premium berbahan fleece, nyaman untuk cuaca dingin",
        "harga": 250000,
        "kategori": "Fashion"
    },
    {
        "nama": "Mouse Gaming Logitech",
        "deskripsi": "Mouse gaming dengan sensor optik presisi tinggi dan RGB lighting",
        "harga": 800000,
        "kategori": "Aksesoris"
    }
]

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
    print("✅ Database initialized")

def add_sample_data():
    """Menambahkan contoh data ke database"""
    conn = sqlite3.connect(DATABASE_URL)
    cursor = conn.cursor()
    
    # Cek apakah sudah ada data
    cursor.execute("SELECT COUNT(*) FROM items")
    count = cursor.fetchone()[0]
    
    if count > 0:
        print(f"⚠️  Database sudah memiliki {count} item(s)")
        confirm = input("Apakah Anda ingin menambahkan data contoh? (y/N): ")
        if confirm.lower() != 'y':
            conn.close()
            return
    
    # Tambahkan data contoh
    for item in sample_items:
        cursor.execute("""
            INSERT INTO items (nama, deskripsi, harga, kategori)
            VALUES (?, ?, ?, ?)
        """, (item["nama"], item["deskripsi"], item["harga"], item["kategori"]))
        print(f"➕ Added: {item['nama']}")
    
    conn.commit()
    
    # Tampilkan statistik
    cursor.execute("SELECT COUNT(*) FROM items")
    total = cursor.fetchone()[0]
    
    cursor.execute("""
        SELECT kategori, COUNT(*) as count 
        FROM items 
        WHERE kategori IS NOT NULL 
        GROUP BY kategori
        ORDER BY count DESC
    """)
    categories = cursor.fetchall()
    
    conn.close()
    
    print(f"\n✅ Data berhasil ditambahkan!")
    print(f"📊 Total items: {total}")
    print(f"📂 Kategori:")
    for cat, count in categories:
        print(f"   - {cat}: {count} items")

def show_all_data():
    """Menampilkan semua data dalam database"""
    conn = sqlite3.connect(DATABASE_URL)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    
    cursor.execute("SELECT * FROM items ORDER BY created_at DESC")
    rows = cursor.fetchall()
    conn.close()
    
    if not rows:
        print("📭 Database kosong")
        return
    
    print(f"📋 Semua data dalam database ({len(rows)} items):")
    print("-" * 100)
    
    for row in rows:
        print(f"ID: {row['id']}")
        print(f"Nama: {row['nama']}")
        print(f"Deskripsi: {row['deskripsi']}")
        print(f"Harga: Rp {row['harga']:,.0f}" if row['harga'] else "Harga: -")
        print(f"Kategori: {row['kategori']}")
        print(f"Created: {row['created_at']}")
        print("-" * 100)

def reset_database():
    """Reset database (hapus semua data)"""
    confirm = input("⚠️  Apakah Anda yakin ingin menghapus SEMUA data? (y/N): ")
    if confirm.lower() != 'y':
        return
    
    conn = sqlite3.connect(DATABASE_URL)
    cursor = conn.cursor()
    
    cursor.execute("DELETE FROM items")
    cursor.execute("DELETE FROM sqlite_sequence WHERE name='items'")  # Reset auto increment
    conn.commit()
    conn.close()
    
    print("🗑️  Database berhasil direset")

def main():
    print("🚀 FastAPI Sample Data Manager")
    print("=" * 50)
    
    while True:
        print("\nPilihan:")
        print("1. Initialize database")
        print("2. Add sample data")
        print("3. Show all data") 
        print("4. Reset database")
        print("5. Exit")
        
        choice = input("\nPilih opsi (1-5): ").strip()
        
        if choice == "1":
            init_db()
        elif choice == "2":
            init_db()  # Pastikan database sudah ada
            add_sample_data()
        elif choice == "3":
            show_all_data()
        elif choice == "4":
            reset_database()
        elif choice == "5":
            print("👋 Selamat tinggal!")
            break
        else:
            print("❌ Pilihan tidak valid")

if __name__ == "__main__":
    main() 