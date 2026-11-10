"""Check the showcase package's required paths and relative Markdown links."""

from pathlib import Path
import re
import sys
import yaml

ROOT = Path(__file__).resolve().parents[2]
REQUIRED = (
    ".github/workflows/docs.yml",
    "docs/index.md",
    "docs/architecture.md",
    "docs/api-design.md",
    "docs/data-model.md",
    "docs/product-spec.md",
    "docs/lessons-learned.md",
    "docs/assets/architecture.svg",
    "docs/assets/code-run-flow.svg",
    "docs/assets/data-model.svg",
    "prototype/learning-flows.pdf",
    "prototype/content-organization.pdf",
    "prototype/early-wireframes.png",
    "screenshots/home-page.png",
    "screenshots/learning-dashboard.png",
    "screenshots/course-view.png",
    "screenshots/coding-playground.png",
    "screenshots/progress-dashboard.png",
    "src/frontend",
    "src/backend plan",
    "src/backend plan/source-materials/openapi.yaml",
    "src/backend plan/source-materials/source-materials-package-88/asyncapi.yaml",
    "mkdocs.yml",
    "README.md",
)


def main() -> int:
    missing = [item for item in REQUIRED if not (ROOT / item).exists()]
    if missing:
        print("Missing required package paths:", ", ".join(missing), file=sys.stderr)
        return 1

    broken = []
    link_pattern = re.compile(r"!?\[[^\]]*\]\(([^)]+)\)")
    for markdown in (ROOT / "docs").rglob("*.md"):
        for target in link_pattern.findall(markdown.read_text(encoding="utf-8")):
            target = target.split("#", 1)[0].strip()
            if not target or "://" in target or target.startswith("mailto:"):
                continue
            if not (markdown.parent / target).resolve().exists():
                broken.append(f"{markdown.relative_to(ROOT)} -> {target}")
    if broken:
        print("Broken relative links:", file=sys.stderr)
        print("\n".join(broken), file=sys.stderr)
        return 1

    contracts = (
        ROOT / "src/backend plan/source-materials/openapi.yaml",
        ROOT / "src/backend plan/source-materials/source-materials-package-88/asyncapi.yaml",
    )
    parsed_contracts = []
    for contract in contracts:
        parsed = yaml.safe_load(contract.read_text(encoding="utf-8"))
        if not isinstance(parsed, dict) or not parsed:
            print(f"Invalid or empty YAML contract: {contract.relative_to(ROOT)}", file=sys.stderr)
            return 1
        parsed_contracts.append(parsed)
    if not str(parsed_contracts[0].get("openapi", "")).startswith("3."):
        print("The preserved OpenAPI contract must declare a 3.x version.", file=sys.stderr)
        return 1
    if not str(parsed_contracts[1].get("asyncapi", "")).startswith("2.") and not str(
        parsed_contracts[1].get("asyncapi", "")
    ).startswith("3."):
        print("The preserved AsyncAPI contract must declare a 2.x or 3.x version.", file=sys.stderr)
        return 1

    print(f"Validated {len(REQUIRED)} required paths, local Markdown links, and API contract YAML.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
