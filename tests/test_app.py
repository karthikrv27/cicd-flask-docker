import pytest
from app import app


@pytest.fixture
def client():
    app.config["TESTING"] = True
    with app.test_client() as client:
        yield client


def test_home(client):
    resp = client.get("/")
    assert resp.status_code == 200
    assert resp.get_json()["message"].startswith("Hello")


def test_health(client):
    resp = client.get("/health")
    assert resp.status_code == 200
    assert resp.get_json()["status"] == "ok"


def test_add(client):
    resp = client.get("/add/3/4")
    assert resp.status_code == 200
    assert resp.get_json()["result"] == 7
