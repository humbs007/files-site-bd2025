from sqlalchemy.orm import sessionmaker
from app.core.config import engine

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Dependency p/ FastAPI
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
