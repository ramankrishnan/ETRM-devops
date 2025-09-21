from fastapi import FastAPI
import logging
import os
import psycopg2
from psycopg2.extras import RealDictCursor

# Setup logger
logger = logging.getLogger("uvicorn")
logger.setLevel(logging.INFO)

app = FastAPI(title="Gravitas ETRM - Trade Capture (dummy)")

# Database URL from environment variable or default
DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://grv_user:grv_pass@db:5432/grv_db")

# Function to get database connection
def get_db_conn():
    try:
        conn = psycopg2.connect(DATABASE_URL)
        return conn
    except Exception as e:
        logger.error("DB connection error: %s", e)
        return None

# Root endpoint
@app.get("/")
def root():
    logger.info("Root endpoint accessed")
    return {"message": "Gravitas ETRM Trade Capture API running"}

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
