import bcrypt
from sqlalchemy.orm import Session
from app.models.database import SessionLocal
from app.models.account_model import Account


# 🔹 Define Admin Credentials
ADMIN_EMAIL = "admin@example.com"
ADMIN_PASSWORD = "admin123"


# 🔹 Hash Password Securely
def hash_password(password: str) -> str:
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')


# 🔹 Create Admin Account
def create_admin_account():
    db: Session = SessionLocal()

    # Check if the account already exists
    existing_admin = db.query(Account).filter(Account.email == ADMIN_EMAIL).first()
    if existing_admin:
        print("✅ Admin account already exists.")
        return
    
    new_admin = Account(
        email=ADMIN_EMAIL,
        hashed_password=hash_password(ADMIN_PASSWORD),
        first_name="Admin",
        last_name="User",
        is_admin=True,
        is_verified=True
    )

    db.add(new_admin)
    db.commit()
    db.refresh(new_admin)
    print("✅ Admin account created successfully.")


if __name__ == "__main__":
    create_admin_account()
