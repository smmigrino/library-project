from sqlalchemy import create_engine, text

# Adjust database name if yours is different
DB_NAME = "library_db"

engine = create_engine(
    f"mysql+mysqlconnector://root:@127.0.0.1:3306/{DB_NAME}",
    echo=False,
    future=True
)

try:
    with engine.connect() as conn:
        result = conn.execute(text("SELECT VERSION()"))
        version = result.scalar()
        print("Connected! MySQL version:", version)
except Exception as e:
    print("Connection error:", e)
