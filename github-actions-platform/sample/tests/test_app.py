from app import health_payload


def test_health_payload():
    payload = health_payload()
    assert payload["status"] == "ok"
    assert payload["service"] == "reusable-ci-sample"
