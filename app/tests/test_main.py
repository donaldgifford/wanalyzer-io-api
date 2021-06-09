from fastapi.testclient import TestClient

from app import main


def test_read_main():
    client = TestClient(main.app)
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Hello World"}
