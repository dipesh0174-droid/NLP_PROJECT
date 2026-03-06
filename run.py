#!/usr/bin/env python3
import os
import sys

def setup_project():
    """Create required directories"""
    dirs = ['data/models', 'data/cache', 'logs', 'tests']
    for d in dirs:
        os.makedirs(d, exist_ok=True)
    
    print("✅ Project directories created")
    print("📦 Install dependencies: pip install -r requirements.txt")
    print("🚀 Run server: python app.py")
    print("🌐 Visit: http://localhost:5000")

if __name__ == "__main__":
    setup_project()
