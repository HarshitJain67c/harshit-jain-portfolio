from __future__ import annotations

from html.parser import HTMLParser
from pathlib import Path
import sys
from urllib.parse import urlparse


ROOT = Path(__file__).resolve().parents[1]
REQUIRED_SECTIONS = {"experience", "capabilities", "project", "education"}


class SiteParser(HTMLParser):
    def __init__(self) -> None:
        super().__init__()
        self.ids: set[str] = set()
        self.links: list[str] = []
        self.assets: list[str] = []
        self.image_alts: list[str | None] = []
        self.title_depth = 0
        self.title = ""
        self.description = ""

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        values = dict(attrs)
        if values.get("id"):
            self.ids.add(values["id"] or "")
        if tag == "a" and values.get("href"):
            self.links.append(values["href"] or "")
        if tag in {"img", "script", "link"}:
            source = values.get("src") or values.get("href")
            if source:
                self.assets.append(source)
        if tag == "img":
            self.image_alts.append(values.get("alt"))
        if tag == "title":
            self.title_depth += 1
        if tag == "meta" and values.get("name") == "description":
            self.description = values.get("content") or ""

    def handle_endtag(self, tag: str) -> None:
        if tag == "title":
            self.title_depth = max(0, self.title_depth - 1)

    def handle_data(self, data: str) -> None:
        if self.title_depth:
            self.title += data


def main() -> int:
    parser = SiteParser()
    parser.feed((ROOT / "index.html").read_text(encoding="utf-8"))
    errors: list[str] = []

    missing_sections = REQUIRED_SECTIONS - parser.ids
    if missing_sections:
        errors.append(f"missing sections: {', '.join(sorted(missing_sections))}")
    if "Harshit Jain" not in parser.title:
        errors.append("page title must identify Harshit Jain")
    if len(parser.description) < 60:
        errors.append("meta description is missing or too short")
    if any(alt is None or not alt.strip() for alt in parser.image_alts):
        errors.append("every image must have useful alternative text")

    for reference in parser.assets:
        parsed = urlparse(reference)
        if parsed.scheme or reference.startswith(("data:", "//")):
            continue
        local_path = ROOT / parsed.path
        if not local_path.is_file():
            errors.append(f"missing local asset: {reference}")

    for link in parser.links:
        if link == "#":
            errors.append("placeholder link found")
        if link.startswith("#") and link[1:] not in parser.ids:
            errors.append(f"link target does not exist: {link}")

    for required_file in ["styles.css", "script.js", "assets/engineering-systems.png"]:
        if not (ROOT / required_file).is_file():
            errors.append(f"required file is missing: {required_file}")

    if errors:
        print("Site validation failed:", file=sys.stderr)
        for error in errors:
            print(f"- {error}", file=sys.stderr)
        return 1
    print(f"Site validation passed: {len(parser.ids)} ids, {len(parser.links)} links, {len(parser.assets)} assets")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
