#!/usr/bin/env python3
"""Generate the static HTML pages from docs-source/*.md.

Zero dependencies. Run from anywhere:  python3 tools/build.py
Supports the Markdown subset the docs use: headings ({#custom-id} optional),
paragraphs, ul/ol (one nesting level), tables, fenced code, blockquotes,
inline code/bold/italic/links, plus two site blocks:
  ![alt](assets/media/file.png "caption") -> linked figure
  ::: note|tip|warning Title ... ::: -> callout
  :::flow ... ::: -> numbered flow
  :::cards ... :::        -> card grid, one "- icon | title | text | link?" per line
"""
import argparse
import html
import re
import struct
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SRC = ROOT / "docs-source"

PRODUCT = "PlayMaker 2 Integration for Game Creator 2"
BRAND_TITLE = "PlayMaker Integration"
BRAND_SUBTITLE = "Game Creator 2 Module"
VERSION = "1.1.3"
SITE = "https://skyward-games.github.io/PlayMaker-Integration-For-GC2-Documentation/"
REPO = "https://github.com/Skyward-Games/PlayMaker-Integration-For-GC2-Documentation"

# (slug, navigation title, meta description), in reading order.
PAGES = [
    ("index", "Introduction", "Connect PlayMaker 2 state orchestration to native Game Creator 2 gameplay, routines, events, and variables."),
    ("getting-started", "Getting Started", "Install the integration, verify selectors, and build a state-driven door with PlayMaker and Game Creator 2."),
    ("fsms-and-gc2", "FSMs & GC2", "Choose ownership, resolve FSMs safely, and map Self, Target, and context between both frameworks."),
    ("integration-workspace", "Integration Workspace", "Use the Action Palette, Templates, Scene Explorer, Diagnostics, and Execution Trace."),
    ("playmaker-to-gc2", "PlayMaker → GC2", "Run native GC2 Actions and Instructions, evaluate Conditions and Properties, and control Core gameplay from an FSM."),
    ("gc2-to-playmaker", "GC2 → PlayMaker", "Reference verified PlayMaker Instructions, Conditions, lifecycle Events, and typed Properties in GC2."),
    ("variable-bridging", "Variables & Property Binder", "Transfer typed values explicitly, work with lists, and configure opt-in Property Binder synchronization."),
    ("events-and-signals", "Events & Signals", "Route local FSM events, bridge broadcasts, native GC2 Signals, and typed Gameplay Events."),
    ("callable-routines", "Callable Routines", "Execute scene and prefab FSMs and author reusable Gameplay Routine assets with typed inputs and outputs."),
    ("singletons-and-utilities", "Singletons & Utilities", "Find FSMs, configure persistent Singletons, wait for lifecycle changes, and transfer collections."),
    ("optional-modules", "Optional Modules", "Understand optional GC2 module detection, adapter boundaries, and native gameplay patterns."),
    ("scripting-api", "Scripting API", "Use confirmed public PlayMakerGC2 types and signatures in custom C# and GC2 Instructions."),
    ("examples", "Examples & Walkthroughs", "Inspect six bundled scenes, their current limitations, and a callable FSM setup exercise."),
    ("best-practices", "Best Practices", "Design clear ownership, lifecycle handling, event boundaries, and efficient variable access."),
    ("troubleshooting", "Troubleshooting", "Diagnose missing or ambiguous FSMs, variables, busy Actions, signal routing, binding, and module imports."),
    ("compatibility", "Compatibility", "Qualified versions, v1.1.3 focused validation, dependencies, and known limitations."),
    ("faq", "FAQ", "Answers about dependencies, FSM targeting, saves, modules, synchronization, and support."),
    ("changelog", "Changelog", "Actual PlayMaker GC2 release history through version 1.1.3, including validation and known limitations."),
]
GROUPS = {0: "Start here", 4: "Workflows", 9: "Reference", 12: "Learn & support"}

SOCIAL = """<div class="social-links">
<a href="https://skywardgames.com.br/" rel="noopener" target="_blank">Website</a>
<a href="https://discord.gg/DTXjRH5TVz" rel="noopener" target="_blank">Support Discord</a>
<a href="https://www.youtube.com/@skywardgames-youtube" rel="noopener" target="_blank">YouTube</a>
<a href="https://x.com/skyward_games" rel="noopener" target="_blank">Twitter/X</a>
</div>"""


def slugify(text):
    text = re.sub(r"<[^>]+>", "", text).lower()
    text = text.replace("→", " to ").replace("&", " and ")
    return re.sub(r"[^a-z0-9]+", "-", text).strip("-")


def inline(text):
    codes = []

    def keep_code(m):
        codes.append("<code>" + html.escape(m.group(1), quote=False) + "</code>")
        return f"\x00{len(codes) - 1}\x00"

    text = re.sub(r"`([^`]+)`", keep_code, text)
    text = html.escape(text, quote=False)

    def link(m):
        label, href = m.group(1), m.group(2)
        if re.match(r"^[a-z][a-z0-9+.-]*:", href, re.I) and not href.startswith(("https://", "http://", "mailto:")):
            raise ValueError(f"Unsupported URL scheme: {href}")
        href = re.sub(r"^([\w-]+)\.md(#.*)?$", lambda h: h.group(1) + ".html" + (h.group(2) or ""), href)
        ext = ' rel="noopener" target="_blank"' if href.startswith("http") else ""
        return f'<a href="{html.escape(html.unescape(href), quote=True)}"{ext}>{label}</a>'

    text = re.sub(r"\[([^\]]+)\]\(([^)\s]+)\)", link, text)
    text = re.sub(r"\*\*(.+?)\*\*", r"<strong>\1</strong>", text)
    text = re.sub(r"(?<![\w*])\*(?!\s)(.+?)(?<!\s)\*(?![\w*])", r"<em>\1</em>", text)
    return re.sub(r"\x00(\d+)\x00", lambda m: codes[int(m.group(1))], text)


def placeholder(caption):
    raise ValueError(f"Replace unfinished screenshot: {caption}")


def media(alt, href, caption):
    path = ROOT / href
    if not path.is_file():
        raise ValueError(f"Missing media: {href}")
    if not href.startswith("assets/"):
        raise ValueError("Media must be local to assets/")
    dims = ""
    if path.suffix == ".png":
        w, h = struct.unpack(">II", path.read_bytes()[16:24])
        dims = f' width="{w}" height="{h}"'
    return (f'<figure class="media-figure"><a class="media-link" href="{html.escape(href)}" target="_blank" rel="noopener" aria-label="Open full size: {html.escape(alt)}">'
            f'<img src="{html.escape(href)}" alt="{html.escape(alt)}"{dims} loading="lazy" decoding="async"></a>'
            f'<figcaption>{inline(caption or alt)} <span class="media-hint">Open image for full size ↗</span></figcaption></figure>')


def cards(lines):
    out = ['<div class="cards-grid">']
    for line in lines:
        parts = [p.strip() for p in line.lstrip("- ").split("|")]
        icon, title, text = parts[0], parts[1], parts[2]
        href = parts[3].replace(".md", ".html") if len(parts) > 3 and parts[3] else None
        tag = f'a class="card" href="{href}"' if href else 'div class="card"'
        close = "a" if href else "div"
        out.append(f'<{tag}>\n<div class="card-icon">{icon}</div>\n<h3 class="card-title">{inline(title)}</h3>\n'
                   f'<p class="card-text">{inline(text)}</p>\n</{close}>')
    out.append("</div>")
    return "\n".join(out)


def table(rows):
    cells = [[c.strip() for c in r.strip().strip("|").split("|")] for r in rows]
    head, body = cells[0], cells[2:]
    if len(cells) < 2 or not all(re.fullmatch(r":?-+:?", c) for c in cells[1]):
        raise ValueError("Table requires a separator row")
    out = ['<div class="table-wrap" tabindex="0" role="region" aria-label="Scrollable reference table">', "<table>", "<thead>", "<tr>"] + [f'<th scope="col">{inline(c)}</th>' for c in head] + ["</tr>", "</thead>", "<tbody>"]
    for r in body:
        out += ["<tr>"] + [f"<td>{inline(c)}</td>" for c in r] + ["</tr>"]
    return "\n".join(out + ["</tbody>", "</table>", "</div>"])


def render_list(lines):
    """lines: raw list lines; supports one nested level via 2+ space indent."""
    ordered = bool(re.match(r"\s*\d+\.", lines[0]))
    tag = "ol" if ordered else "ul"
    out, i = [f"<{tag}>"], 0
    while i < len(lines):
        item = re.sub(r"^\s*(?:[-*]|\d+\.)\s+", "", lines[i])
        i += 1
        children = []
        while i < len(lines) and re.match(r"^\s{2,}", lines[i]):
            children.append(lines[i].strip() if re.match(r"^\s*(?:[-*]|\d+\.)\s", lines[i]) else lines[i])
            i += 1
        sub = render_list(children) if children else ""
        out.append(f"<li>{inline(item)}{sub}</li>")
    out.append(f"</{tag}>")
    return "\n".join(out)


def convert(md):
    lines = md.splitlines()
    out, toc, title, i = [], [], None, 0
    used_ids = set()
    is_list = re.compile(r"^\s*(?:[-*]|\d+\.)\s+")
    while i < len(lines):
        line = lines[i]
        if not line.strip():
            i += 1
            continue
        if line.startswith("```"):
            lang = line[3:].strip() or "text"
            body = []
            i += 1
            while i < len(lines) and not lines[i].startswith("```"):
                body.append(lines[i])
                i += 1
            if i == len(lines):
                raise ValueError("Unclosed code fence")
            i += 1
            out.append(f'<pre><code class="language-{lang}">' + html.escape("\n".join(body), quote=False) + "\n</code></pre>")
            continue
        m = re.match(r"^(#{1,4})\s+(.*?)(?:\s+\{#([\w-]+)\})?\s*$", line)
        if m:
            level, text = len(m.group(1)), m.group(2)
            base = m.group(3) or slugify(text)
            hid, suffix = base, 2
            while hid in used_ids:
                hid = f"{base}-{suffix}"
                suffix += 1
            used_ids.add(hid)
            if level == 1:
                if title:
                    raise ValueError("Only one H1 is allowed per page")
                title = text
            elif level in (2, 3):
                toc.append((level, hid, text))
            out.append(f'<h{level} id="{hid}">{inline(text)}<a aria-label="Link to {html.escape(text)}" class="anchor" href="#{hid}">#</a></h{level}>')
            i += 1
            continue
        if line.strip() == ":::cards":
            block = []
            i += 1
            while i < len(lines) and lines[i].strip() != ":::":
                if lines[i].strip():
                    block.append(lines[i].strip())
                i += 1
            if i == len(lines):
                raise ValueError("Unclosed cards block")
            i += 1
            out.append(cards(block))
            continue
        m = re.fullmatch(r'!\[([^\]]+)\]\(([^\s)]+)(?: "([^"]+)")?\)', line)
        if m:
            out.append(media(*m.groups()))
            i += 1
            continue
        if line.startswith("::: "):
            kind, _, label = line[4:].partition(" ")
            if kind not in ("note", "tip", "warning"):
                raise ValueError(f"Unknown callout: {kind}")
            block = []
            i += 1
            while i < len(lines) and lines[i].strip() != ":::":
                block.append(lines[i]); i += 1
            if i == len(lines):
                raise ValueError("Unclosed callout")
            _, body, _ = convert("\n".join(block))
            out.append(f'<aside class="callout {kind}" aria-label="{html.escape(label or kind.title())}"><strong class="callout-title">{inline(label or kind.title())}</strong>{body}</aside>')
            i += 1
            continue
        if line.strip() == ":::flow":
            flow = ['<ol class="flow" aria-label="Integration flow">']
            i += 1
            while i < len(lines) and lines[i].strip() != ":::":
                if lines[i].strip():
                    icon, heading, desc = [x.strip() for x in lines[i].lstrip("- ").split("|")]
                    flow.append(f'<li><span class="flow-icon" aria-hidden="true">{html.escape(icon)}</span><strong>{inline(heading)}</strong><span>{inline(desc)}</span></li>')
                i += 1
            if i == len(lines):
                raise ValueError("Unclosed flow block")
            out.append("\n".join(flow + ["</ol>"]))
            i += 1
            continue
        m = re.match(r"^\[SCREENSHOT:\s*(.*)\]\s*$", line)
        if m:
            out.append(placeholder(m.group(1)))
            i += 1
            continue
        if line.startswith("|"):
            rows = []
            while i < len(lines) and lines[i].startswith("|"):
                rows.append(lines[i])
                i += 1
            out.append(table(rows))
            continue
        if line.startswith(">"):
            block = []
            while i < len(lines) and lines[i].startswith(">"):
                block.append(lines[i][1:].strip())
                i += 1
            paras = "\n".join(block).split("\n\n")
            out.append("<blockquote>" + "".join(f"<p>{inline(' '.join(p.split()))}</p>" for p in paras) + "</blockquote>")
            continue
        if is_list.match(line):
            block = []
            while i < len(lines) and (is_list.match(lines[i]) or (lines[i].startswith("  ") and lines[i].strip())):
                block.append(lines[i])
                i += 1
            out.append(render_list(block))
            continue
        para = []
        while i < len(lines) and lines[i].strip() and not re.match(r"^(#|```|\||>|:::|!\[|\[SCREENSHOT)", lines[i]) and not is_list.match(lines[i]):
            para.append(lines[i].strip())
            i += 1
        if not para:
            raise ValueError(f"Unsupported block: {line}")
        out.append(f"<p>{inline(' '.join(para))}</p>")
    return title, "\n\n".join(out), toc


def brand():
    return ('<a class="brand" href="index.html" aria-label="PlayMaker documentation home">'
            '<img class="brand-logo" src="assets/media/product-icon.png" width="42" height="42" alt="">'
            f'<span><span class="brand-title">{BRAND_TITLE}</span><span class="brand-subtitle">{BRAND_SUBTITLE}</span></span></a>')


def page_html(idx, title, body, toc):
    slug, nav_title, desc = PAGES[idx]
    theme_btn = '<button class="theme-toggle" data-theme-toggle type="button"><span aria-hidden="true" class="icon">◐</span><span class="label">Theme</span></button>'
    nav, group = [], ''
    for j, (s, t, _) in enumerate(PAGES):
        if j in GROUPS:
            if j: nav.append('</section>')
            group = GROUPS[j]
            nav.append(f'<section class="nav-group"><h2 class="nav-group-title">{group}</h2>')
        active = ' class="nav-link active" aria-current="page"' if j == idx else ' class="nav-link"'
        nav.append(f'<a{active} href="{s}.html">{html.escape(t)}</a>')
    nav.append('</section>')
    page_group = GROUPS[max(j for j in GROUPS if j <= idx)]
    pn = []
    for offset, css, direction in [(-1, 'prev', 'Previous'), (1, 'next', 'Next')]:
        if 0 <= idx + offset < len(PAGES):
            s, t, _ = PAGES[idx + offset]
            arrow = '←' if offset < 0 else '→'
            pn.append(f'<a class="{css}" href="{s}.html"><span class="label">{direction}</span><span class="title">{html.escape(t)} {arrow}</span></a>')
    toc_html = '\n'.join(f'<a class="toc-h{lvl}" href="#{hid}">{inline(text)}</a>' for lvl, hid, text in toc)
    hero = ''
    if slug == 'index':
        hero = ('<section class="hero"><span class="eyebrow">Two frameworks. One gameplay workflow.</span>'
                '<h1 id="introduction">State in PlayMaker.<br><span>Gameplay in Game Creator.</span></h1>'
                '<p class="hero-lead">Connect your state machines to native Actions, Conditions, Properties, and Signals—with explicit control over context, data, and execution.</p>'
                '<div class="hero-actions"><a class="button primary" href="getting-started.html">Build your first workflow →</a>'
                '<a class="button secondary" href="examples.html">Explore the examples</a></div>'
                '<div class="feature-chips"><span>PlayMaker 2</span><span>Game Creator 2 Core</span><span>Unity 6</span><span>v1.1.3</span></div></section>')
        body = re.sub(r'^<h1\b.*?</h1>\s*', '', body, count=1, flags=re.S)
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{html.escape(title)} · {PRODUCT}</title>
<meta name="description" content="{html.escape(desc)}">
<meta name="theme-color" content="#f4faff">
<link rel="canonical" href="{SITE}{slug}.html">
<meta property="og:title" content="{html.escape(title)} · PlayMaker GC2">
<meta property="og:description" content="{html.escape(desc)}">
<meta property="og:type" content="website">
<meta property="og:url" content="{SITE}{slug}.html">
<meta property="og:image" content="{SITE}assets/media/bridge-overview.png">
<link rel="icon" href="assets/media/product-icon.png" type="image/png">
<script>try{{const t=localStorage.getItem('playmaker-gc2-docs-theme');document.documentElement.dataset.theme=t==='dark'||t==='light'?t:(matchMedia('(prefers-color-scheme: dark)').matches?'dark':'light');}}catch{{document.documentElement.dataset.theme='light';}}</script>
<link rel="stylesheet" href="assets/style.css">
<script src="assets/script.js" defer></script>
</head>
<body>
<a class="skip-link" href="#main-content">Skip to content</a>
<div class="reading-progress" data-reading-progress aria-hidden="true"></div>
<header class="topbar">{brand()}<div class="topbar-actions">{theme_btn}<button class="menu-btn" data-menu type="button" aria-controls="docs-sidebar" aria-expanded="false">Menu</button></div></header>
<div class="layout">
<aside class="sidebar" id="docs-sidebar" aria-label="Documentation sidebar">
<button class="sidebar-close" data-close-menu type="button">Close menu ×</button>{brand()}<span class="version-label">Documentation <strong>v{VERSION}</strong></span>
<div class="search-wrap"><label class="sr-only" for="page-search">Filter documentation pages</label><input class="search" id="page-search" data-search type="search" placeholder="Filter pages…  /" aria-describedby="search-status"><p id="search-status" class="search-status" role="status" aria-live="polite"></p></div>
<nav class="nav" aria-label="Documentation">{''.join(nav)}</nav>
<div class="sidebar-actions">{theme_btn}<a class="source-link" href="{REPO}" target="_blank" rel="noopener">Documentation on GitHub ↗</a></div>
<div class="sidebar-footer"><p>Skyward Games</p>{SOCIAL}</div>
</aside>
<div class="content"><main class="page" id="main-content" tabindex="-1">
<div class="page-meta"><span>{page_group}</span><span>PlayMaker GC2 · v{VERSION}</span></div>
{hero}{body}
<nav class="page-nav" aria-label="Page navigation">{''.join(pn)}</nav>
<footer class="page-footer"><span>© Skyward Games · PlayMaker GC2</span><a href="{REPO}/blob/main/docs-source/{slug}.md" target="_blank" rel="noopener">Edit this page ↗</a></footer>
</main><aside class="toc" aria-label="On this page"><span class="toc-title">On this page</span><nav>{toc_html}</nav><a class="back-to-top" href="#main-content">Back to top ↑</a></aside>
</div></div><div class="mobile-scrim" data-scrim aria-hidden="true"></div>
</body>
</html>
"""


def outputs():
    for idx, (slug, _, _) in enumerate(PAGES):
        title, body, toc = convert((SRC / f"{slug}.md").read_text(encoding="utf-8"))
        if not title: raise ValueError(f'Missing H1: {slug}')
        yield ROOT / f"{slug}.html", page_html(idx, title, body, toc)
    urls = ''.join(f'<url><loc>{SITE}{slug}.html</loc></url>' for slug, *_ in PAGES)
    yield ROOT / 'sitemap.xml', f'<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">{urls}</urlset>\n'
    yield ROOT / 'robots.txt', f'User-agent: *\nAllow: /\nSitemap: {SITE}sitemap.xml\n'


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--check', action='store_true', help='Check generated files without writing')
    args = parser.parse_args()
    stale = []
    for path, content in outputs():
        if args.check:
            if not path.exists() or path.read_text(encoding='utf-8') != content: stale.append(path.name)
        else:
            path.write_text(content, encoding='utf-8', newline='\n')
    if stale: parser.exit(1, 'Stale generated files: ' + ', '.join(stale) + '\n')
    print(f'{"Verified" if args.check else "Built"} {len(PAGES)} pages, sitemap, and robots.txt')


if __name__ == '__main__':
    main()
