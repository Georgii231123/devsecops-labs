from app.main import app


def test_health() -> None:
    client = app.test_client()
    response = client.get("/healthz")
    assert response.status_code == 200
    assert response.get_json() == {"status": "ok"}
