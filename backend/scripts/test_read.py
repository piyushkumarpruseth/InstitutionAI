
from sqlalchemy import select

from backend.database import SessionLocal
from backend.model import Institution

# Create database session
db = SessionLocal()

try:
    # Fetch all institutions
    statement = select(Institution)

    institutions = db.scalars(statement).all()

    # Display institutions
    for institution in institutions:
        print("------------------------")
        print("ID:", institution.id)
        print("Name:", institution.name)
        print("Type:", institution.institution_type)
        print("Email:", institution.email)

except Exception as e:
    print("Error:", e)

finally:
    db.close()
