from sqlalchemy import update
from backend.database import SessionLocal
from backend.model import Institution

db = SessionLocal()

institution_id =1

try:
    statement = (
    update(Institution)
    .where(Institution.id == institution_id)
    .values(email="school@gmail.com")
    )

    db.execute(statement)

    db.commit()

except Exception as e:
    db.rollback()
    print("Error" , e)

finally:
    db.close()    

