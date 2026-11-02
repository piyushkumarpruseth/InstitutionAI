from backend.database import SessionLocal
from backend.model import Institution

db = SessionLocal()

try:
    new_institution = Institution(
        name = "SQLAlchemy Demo School",
        institution_type = "School",
        email = "sqlalchemy_demo@gmail.com",
    )

    db.add(new_institution)

    db.commit()

    db.refresh(new_institution)

except Exception as e:
    db.rollback()
    print("Error" , e)

finally:
    db.close()        