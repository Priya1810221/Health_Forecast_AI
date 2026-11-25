import os
import sys

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app import models, security

url = os.getenv("DATABASE_URL")
email = os.getenv("ADMIN_EMAIL")
name = os.getenv("ADMIN_NAME", "Admin")
password = os.getenv("ADMIN_PASSWORD")

if not (url and email and password):
    print("Admin settings not provided, skipping.")
    sys.exit(0)

db = sessionmaker(bind=create_engine(url))()

if db.query(models.User).filter(models.User.email == email).first():
    print("Admin already exists, skipping.")
else:
    db.add(models.User(
        full_name=name,
        email=email,
        hashed_password=security.hash_password(password),
        role="system_admin",
    ))
    db.commit()
    print("Admin created:", email)