from pathlib import Path

from bootstrap import render_tree
from scripts.validate_service import validate


def test_template_renders_and_validates(tmp_path: Path) -> None:
    template = Path(__file__).parents[1] / "template" / "service"
    destination = tmp_path / "orders-api"
    render_tree(
        template,
        destination,
        {
            "service_name": "Orders API",
            "service_slug": "orders-api",
            "owner": "orders-team",
            "port": "8080",
        },
    )
    assert validate(destination) == []
    assert "orders-api" in (destination / "service.yaml").read_text(encoding="utf-8")
