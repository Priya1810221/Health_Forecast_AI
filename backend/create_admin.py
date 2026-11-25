import os
import sys
from getpass import getpass

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app import models, security

url = os.getenv("DATABASE_URL")
if not url:
    sys.exit("DATABASE_URL is not set. Set it first (see the steps).")

engine = create_engine(url)
db = sessionmaker(bind=engine)()

email = input("Admin email: ").strip()
name = input("Full name: ").strip()
password = getpass("Password (hidden while typing): ")

if db.query(models.User).filter(models.User.email == email).first():
    sys.exit("That email already exists.")

user = models.User(
    full_name=name,
    email=email,
    hashed_password=security.hash_password(password),
    role="system_admin",
)
db.add(user)
db.commit()
print("Admin created. You can log in with", email)