#!/usr/bin/env python3
"""
Script untuk menjalankan FastAPI server
Jalankan dengan: python run.py
"""

import uvicorn
from main import app

if __name__ == "__main__":
    print("🚀 Memulai FastAPI server...")
    print("📍 Server akan berjalan di: http://localhost:8000")
    print("📖 Dokumentasi API: http://localhost:8000/docs")
    print("🔧 Admin Panel: http://localhost:8000/redoc")
    print("\n⏹️  Tekan Ctrl+C untuk menghentikan server\n")
    
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,  # Auto-reload saat development
        log_level="info"
    ) 