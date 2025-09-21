# trade-capture/app/tests/test_dummy.py

from app.main import app   # <-- absolute import
from fastapi.testclient import TestClient

client = TestClient(app)

def test_ping():
    res = client.get("/ping")
    assert res.status_code == 200
    assert res.json()["status"] == "ok"
