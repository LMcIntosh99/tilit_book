from fastapi import FastAPI, UploadFile, Form
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
import shutil
import os
import psycopg2
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()
DB_PASSWORD = os.getenv("DB_PASSWORD")

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

# Mount static files
app.mount("/uploads", StaticFiles(directory=UPLOAD_DIR), name="uploads")

# DB connection
conn = psycopg2.connect(
    dbname="tilit_book_db", user="t_admin", password=DB_PASSWORD, host="localhost"
)
cur = conn.cursor()

# Create table if not exists
cur.execute("""
CREATE TABLE IF NOT EXISTS submissions (
    id SERIAL PRIMARY KEY,
    image_url TEXT,
    location TEXT,
    lat float,
    lng float,
    comment TEXT,
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
)
""")
conn.commit()


@app.post("/upload")
async def upload(image: UploadFile, location: str = Form(...), comment: str = Form("")):
    filename = f"{datetime.utcnow().timestamp()}_{image.filename}"
    file_path = os.path.join(UPLOAD_DIR, filename)

    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(image.file, buffer)

    cur.execute("INSERT INTO submissions (image_url, location, comment) VALUES (%s, %s, %s)",
                (f"uploads/{filename}", location, comment))
    conn.commit()
    return {"status": "ok"}


@app.get("/submissions")
def get_submissions():
    cur.execute("SELECT id, image_url, location, comment, timestamp FROM submissions ORDER BY timestamp DESC")
    rows = cur.fetchall()
    return [
        {
            "id": r[0],
            "image_url": r[1],
            "location": r[2],
            "comment": r[3],
            "timestamp": r[4].isoformat()
        } for r in rows
    ]
