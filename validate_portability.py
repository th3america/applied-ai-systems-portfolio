"""Validate the structural minimum of a PortableScaffold/1 repository."""
import argparse
import json
import re
from pathlib import Path

REQUIRED = {
    "protocol", "project", "entrypoints", "minimum_runtime", "configuration",
    "state", "adapters", "invariants", "verification_commands",
    "known_platform_variance", "authority_boundary",
}
PERSONAL_PATH = re.compile(r"(?:[A-Za-z]:\\Users\\[^\\]+|/Users/[^/]+|/home/[^/]+)")


def validate(root):
    root = Path(root).resolve()
    manifest_path = root / "portability.json"
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    errors = []
    missing = sorted(REQUIRED - manifest.keys())
    if missing:
        errors.append(f"missing fields: {', '.join(missing)}")
    if manifest.get("protocol") != "PortableScaffold/1":
        errors.append("protocol must be PortableScaffold/1")
    for item in manifest.get("entrypoints", []):
        if Path(item).is_absolute() or not (root / item).exists():
            errors.append(f"entrypoint is missing or absolute: {item}")
    encoded = json.dumps(manifest, ensure_ascii=False)
    if PERSONAL_PATH.search(encoded):
        errors.append("manifest contains a personal absolute path")
    for field in ("entrypoints", "adapters", "invariants", "verification_commands"):
        if not isinstance(manifest.get(field), list) or not manifest.get(field):
            errors.append(f"{field} must be a nonempty list")
    return {"protocol": "PortableScaffoldValidation/1", "root": str(root),
            "project": manifest.get("project"), "valid": not errors,
            "errors": errors}


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("root", nargs="?", default=".")
    result = validate(parser.parse_args().root)
    print(json.dumps(result, indent=2))
    raise SystemExit(0 if result["valid"] else 1)
