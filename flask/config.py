# config.py
import os

class Config:
    SQLALCHEMY_DATABASE_URI = os.getenv(
        'DATABASE_URL',
        'postgresql://postgres:qaz123!@192.168.234.131:5432/inventory'
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False
