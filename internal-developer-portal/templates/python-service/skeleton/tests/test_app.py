from pathlib import Path


def test_service_source_has_health_endpoint() -> None:
    source = (Path(__file__).parents[1] / "src" / "main.py").read_text()
    assert '"/healthz"' in source
