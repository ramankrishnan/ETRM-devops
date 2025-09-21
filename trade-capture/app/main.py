from fastapi import FastAPI
from fastapi.responses import HTMLResponse
import logging
import os
import psycopg2
from psycopg2.extras import RealDictCursor

# Setup logger
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

# Root endpoint - HTML page with background and centered bold title
@app.get("/", response_class=HTMLResponse)
def root():
    html_content = """
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <title>Gravitas ETRM</title>
        <style>
            body {
                background-image: url('https://images.unsplash.com/photo-1507525428034-b723cf961d3e'); /* Change this to your image */
                background-size: cover;
                background-repeat: no-repeat;
                background-position: center;
                display: flex;
                justify-content: center;
                align-items: center;
                height: 100vh;
                margin: 0;
                font-family: Arial, sans-serif;
            }
            h1 {
                color: white;
                font-size: 48px;
                font-weight: bold;
                text-align: center;
                text-shadow: 2px 2px 5px black;
            }
            p {
                color: white;
                font-size: 24px;
                font-weight: bold;
                text-align: center;
                text-shadow: 1px 1px 3px black;
            }
        </style>
    </head>
    <body>
        <div>
            <h1>DevOps in Gravitas ETRM</h1>
            <p>Welcome to the Trade Capture Service</p>
        </div>
    </body>
    </html>
    """
    return HTMLResponse(content=html_content)

# Ping endpoint
@app.get("/ping")
def ping():
    logger.info("Ping received")
    return {"status": "ok", "service": "trade-capture"}

# Health endpoint - checks database connection
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

# Optional DB test route
@app.get("/db")
def db_test():
    conn = get_db_conn()
    if conn:
        conn.close()
        logger.info("DB reachable")
        return {"status": "db reachable"}
    else:
        logger.error("DB unreachable")
        return {"status": "db unreachable"}
