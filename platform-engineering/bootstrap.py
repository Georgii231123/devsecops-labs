from __future__ import annotations

import argparse
import shutil
from pathlib import Path

TOKENS = {
    "__SERVICE_NAME__": "service_name",
    "__SERVICE_SLUG__": "service_slug",
    "__OWNER__": "owner",
    "__PORT__": "port",
}


def render_tree(template: Path, destination: Path, values: dict[str, str]) -> None:
    if destination.exists():
        raise FileExistsError(f"destination already exists: {destination}")
    shutil.copytree(template, destination)
    for path in destination.rglob("*"):
        if not path.is_file():
            continue
        try:
            text = path.read_text(encoding="utf-8")
        except UnicodeDecodeError:
            continue
        for token, key in TOKENS.items():
            text = text.replace(token, values[key])
        path.write_text(text, encoding="utf-8")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Generate a service from the platform golden path")
    parser.add_argument("service_name")
    parser.add_argument("--owner", required=True)
    parser.add_argument("--port", type=int, default=8080)
    parser.add_argument("--output", type=Path, default=Path("generated"))
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    slug = args.service_name.strip().lower().replace("_", "-").replace(" ", "-")
    if not slug or any(ch not in "abcdefghijklmnopqrstuvwxyz0123456789-" for ch in slug):
        raise SystemExit("service name must contain only letters, digits, spaces, '_' or '-'")
    if not 1 <= args.port <= 65535:
        raise SystemExit("port must be between 1 and 65535")

    template = Path(__file__).parent / "template" / "service"
    destination = args.output / slug
    values = {
        "service_name": args.service_name,
        "service_slug": slug,
        "owner": args.owner,
        "port": str(args.port),
    }
    args.output.mkdir(parents=True, exist_ok=True)
    render_tree(template, destination, values)
    print(f"created {destination}")


if __name__ == "__main__":
    main()
