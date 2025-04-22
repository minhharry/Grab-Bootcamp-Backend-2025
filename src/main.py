from routers import dummy 
from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from database import SessionLocal, Base, engine
from sqlalchemy import text

app = FastAPI()

app.include_router(dummy.router)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()



@app.get("/")
def read_root(db: Session = Depends(get_db)):
    try:
        result = db.execute(text("SELECT 1")).scalar()
        return {"message": "Connected to DB!", "result": result}
    except Exception as e:
        return {"error": str(e)}

