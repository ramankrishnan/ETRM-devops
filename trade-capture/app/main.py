from fastapi import FastAPI
from fastapi.responses import HTMLResponse
import logging
import os
import psycopg2
from psycopg2.extras import RealDictCursor

logger = logging.getLogger("uvicorn")
logger.setLevel(logging.INFO)

app = FastAPI(title="Gravitas ETRM - Trade Capture (dummy)")

DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://grv_user:grv_pass@db:5432/grv_db")

def get_db_conn():
    try:
        conn = psycopg2.connect(DATABASE_URL)
        return conn
    except Exception as e:
        logger.error("DB connection error: %s", e)
        return None

@app.get("/ping")
def ping():
    logger.info("Ping received")
    return {"status": "ok", "service": "trade-capture"}

@app.get("/health")
def health():
    conn = get_db_conn()
    if conn:
        try:
            cur = conn.cursor(cursor_factory=RealDictCursor)
            cur.execute("SELECT 1 as result;")
            cur.close()
            conn.close()
            logger.info("DB health OK")
            return {"status": "ok", "db": "reachable"}
        except Exception as e:
            logger.error("DB health failed: %s", e)
            return {"status": "fail", "error": str(e)}
    else:
        return {"status": "fail", "error": "cannot connect to db"}

# HTML page endpoint
@app.get("/", response_class=HTMLResponse)
def homepage():
    html_content = """
    <html>
        <head>
            <title>Gravitas ETRM - Trade Capture</title>
            <style>
                body {
                    display: flex;
                    justify-content: center;
                    align-items: center;
                    height: 100vh;
                    margin: 0;
                    background-image: url('https://images.unsplash.com/photo-1602524209260-fbcd237c3aaf');
                    background-size: cover;
                    background-repeat: no-repeat;
                    font-family: Arial, sans-serif;
                }
                h1 {
                    color: white;
                    font-size: 3rem;
                    font-weight: bold;
                    text-align: center;
                    text-shadow: 2px 2px 4px rgba(0,0,0,0.7);
                    border: 2px solid white;
                    padding: 30px 50px;
                    border-radius: 20px;
                    background-color: rgba(0,0,0,0.5);
                }
            </style>
        </head>
        <body>
            <h1>DevOps in Gravitas ETRM</h1>
        </body>
    </html>
    """
    return HTMLResponse(content=html_content)
