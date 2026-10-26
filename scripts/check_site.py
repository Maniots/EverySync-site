"""Check the publishable static directory without third-party dependencies."""
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import unquote, urlsplit

ROOT = Path(__file__).resolve().parents[1] / "public"


class Page(HTMLParser):
    def __init__(self, path):
        super().__init__(convert_charrefs=True)
        self.path, self.ids, self.links = path, set(), []
        self.title = self.h1 = self.lang = 0
        self.errors = []

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if attrs.get("id"):
            if attrs["id"] in self.ids:
                self.errors.append(f"Duplicate ID: {attrs['id']}")
            self.ids.add(attrs["id"])
        self.title += tag == "title"
        self.h1 += tag == "h1"
        self.lang += tag == "html" and attrs.get("lang") == "en"
        if tag in {"script", "iframe", "form"}:
            self.errors.append(f"Unexpected active or third-party content: {tag}")
        if tag == "img" and "alt" not in attrs:
            self.errors.append("Image missing alt attribute")
        for field in ("href", "src"):
            if attrs.get(field):
                self.links.append(attrs[field])
                if any(character.isspace() for character in attrs[field]):
                    self.errors.append(f"Whitespace in URL: {attrs[field]}")
                if field == "src" and urlsplit(attrs[field]).netloc:
                    self.errors.append("Remote resource contradicts website privacy disclosure")


pages = {}
for path in ROOT.glob("*.html"):
    page = Page(path)
    page.feed(path.read_text(encoding="utf-8"))
    pages[path.resolve()] = page
assert {path.name for path in pages} == {"index.html", "privacy.html"}
errors = []
for path, page in pages.items():
    errors.extend(f"{path.name}: {message}" for message in page.errors)
    if (page.title, page.h1, page.lang) != (1, 1, 1):
        errors.append(f"{path.name}: expected one title, h1 and English document language")
    for link in page.links:
        url = urlsplit(link)
        if url.scheme or url.netloc:
            if url.scheme != "https":
                errors.append(f"{path.name}: external link must use HTTPS")
            continue
        target = (path.parent / unquote(url.path)).resolve() if url.path else path
        if target.is_dir():
            target /= "index.html"
        if not target.is_relative_to(ROOT.resolve()) or not target.is_file():
            errors.append(f"{path.name}: missing or escaping local resource {link}")
        elif url.fragment and target in pages and unquote(url.fragment) not in pages[target].ids:
            errors.append(f"{path.name}: missing fragment {link}")
css = (ROOT / "styles.css").read_text(encoding="utf-8")
if "@import" in css or "url(" in css:
    errors.append("Stylesheet must not load unreviewed resources")
if errors:
    raise SystemExit("\n".join(errors))
print(f"Checked {len(pages)} pages: local resources, links, anchors, metadata and passive content OK.")
