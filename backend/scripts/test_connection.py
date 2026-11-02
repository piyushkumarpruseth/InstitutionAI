from sqlalchemy import text 
from backend.database import engine

try:
    with engine.connect() as connection:
        result = connection.execute(text("SELECT VERSION()"))

        print("MySQL Connected Successfully!")
        print("MySQL Version:", result.scalar())

except Exception as e:
    print("Database Connection Failed!")
    print("Error:", e)