import sys
from pathlib import Path

project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from src.app import app


def test_homepage_loads():
    """Basic smoke test: the homepage should return HTTP 200."""
    client = app.test_client()
    resp = client.get("/")
    assert resp.status_code == 200
    assert b"PGA Stat Leaders" in resp.data  

def test_health_endpoint():
    """Test the health endpoint returns HTTP 200."""
    client = app.test_client()
    resp = client.get("/health")
    assert resp.status_code == 200
    assert resp.json == {"status": "ok"}

def test_homepage_with_year_query_param():
    """
    The app should handle a specific year query parameter without error.
    We use 2024 as an example, but any year in your data should work.
    """
    client = app.test_client()
    resp = client.get("/?year=2024")
    assert resp.status_code == 200
    assert b"2024" in resp.data