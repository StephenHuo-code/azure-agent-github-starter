
import requests

def test_healthz():
    r = requests.get("http://localhost:8000/healthz", timeout=5)
    assert r.status_code == 200
    assert r.json().get("ok") is True
