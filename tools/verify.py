#!/usr/bin/env python3
"""Verify the generated documentation using only Python's standard library."""
from collections import Counter
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import unquote, urlsplit
import re
import sys

import build


class Page(HTMLParser):
    def __init__(self, text):
        super().__init__(convert_charrefs=True)
        self.ids, self.refs, self.images, self.meta = [], [], [], {}
        self.h1, self.main, self.canonical, self.title = 0, 0, None, False
        self.feed(text)

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if "id" in attrs:
            self.ids.append(attrs["id"])
        if tag == "h1":
            self.h1 += 1
        if tag == "main":
            self.main += 1
        if tag == "title":
            self.title = True
        if tag == "meta":
            self.meta[attrs.get("name", attrs.get("property", ""))] = attrs.get("content", "")
        if tag == "link" and attrs.get("rel") == "canonical":
            self.canonical = attrs.get("href")
        if tag == "img":
            self.images.append(attrs)
        for key in ("href", "src"):
            if key in attrs:
                self.refs.append(attrs[key])


def verify(root=build.ROOT):
    errors = []
    expected = {slug + ".html" for slug, *_ in build.PAGES}
    actual = {p.name for p in root.glob("*.html")}
    if actual != expected:
        errors.append(f"HTML page mismatch: {sorted(actual ^ expected)}")
    pages = {}
    for name in sorted(expected):
        path = root / name
        if not path.is_file():
            errors.append(f"Missing page: {name}")
            continue
        text = path.read_text(encoding="utf-8")
        page = pages[name] = Page(text)
        if page.h1 != 1 or page.main != 1:
            errors.append(f"{name}: expected one H1 and one main")
        duplicates = [hid for hid, count in Counter(page.ids).items() if count > 1]
        if duplicates:
            errors.append(f"{name}: duplicate IDs: {duplicates}")
        if not page.title or not page.meta.get("description") or not page.meta.get("viewport"):
            errors.append(f"{name}: required page metadata missing")
        if page.canonical != build.SITE + name:
            errors.append(f"{name}: canonical URL mismatch")
        if re.search(r"\[SCREENSHOT:|Screenshot needed|planned feature set|FsmBridge\.|FsmValueConverter\.|IFsmValueAdapter", text):
            errors.append(f"{name}: unfinished/speculative content")
        for img in page.images:
            if not img.get("alt") and img.get("src") != "assets/media/product-icon.png":
                errors.append(f"{name}: image requires alt text")
            if not img.get("width") or not img.get("height"):
                errors.append(f"{name}: image dimensions missing")
    references = 0
    for name, page in pages.items():
        for href in page.refs:
            parsed = urlsplit(href)
            if parsed.scheme or parsed.netloc:
                continue
            references += 1
            relative = unquote(parsed.path)
            target = (root / name).parent / relative if relative else root / name
            target = target.resolve()
            if not target.is_relative_to(root.resolve()):
                errors.append(f"{name}: reference outside site: {href}")
            elif not target.is_file():
                errors.append(f"{name}: missing local reference: {href}")
            elif parsed.fragment and target.suffix == ".html":
                other = pages.get(target.name)
                if other and unquote(parsed.fragment) not in other.ids:
                    errors.append(f"{name}: missing anchor: {href}")
            if relative.endswith(".md"):
                errors.append(f"{name}: unconverted Markdown link: {href}")
    for path, expected_text in build.outputs():
        if not path.exists() or path.read_text(encoding="utf-8") != expected_text:
            errors.append(f"Stale generated file: {path.name}")
    return errors, references


if __name__ == "__main__":
    failures, references = verify()
    if failures:
        print("\n".join(failures))
        sys.exit(1)
    print(f"Verified {len(build.PAGES)} pages and {references} local references; metadata, images, anchors, and generated output are valid")
