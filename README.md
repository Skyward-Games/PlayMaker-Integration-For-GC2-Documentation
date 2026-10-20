# PlayMaker 2 Integration for Game Creator 2 — Documentation

English documentation for **PlayMaker GC2 v1.1.3**, by Skyward Games.

- [Read the documentation](https://skyward-games.github.io/PlayMaker-Integration-For-GC2-Documentation/)
- [Support Discord](https://discord.gg/DTXjRH5TVz)
- [Skyward Games](https://skywardgames.com.br/)

## Contents

Eighteen pages cover installation, framework ownership and context, the Integration Workspace, both scripting directions, variables and Property Binder, events, callable routines, Singletons, utilities, optional modules, C#, six reference scenes, troubleshooting, compatibility, and release history.

The site uses Asset References documentation as its main layout reference and Animation Montages documentation for introductory presentation and walkthrough structure. It retains its own PlayMaker cyan styling.

## Edit and Build

Requires Python 3.10+; the build has no third-party dependencies.

```bash
python tools/build.py
python tools/build.py --check
python tools/verify.py
python -m unittest discover -s tools -p "test_*.py"
```

Content lives in `docs-source/<page>.md`. Edit Markdown and regenerate HTML; commit both. Page order, navigation groups, metadata, and public URLs are defined in `tools/build.py`. Never edit generated HTML as the source of a change.

The small Markdown renderer supports headings with optional `{#custom-id}`, paragraphs, one-level nested lists, tables, fenced code, blockquotes, links, and inline formatting. Duplicate heading slugs receive numeric suffixes.

### Media

Use a standalone image block; paths are relative to the site root:

```text
![Descriptive alt text](assets/media/image.png "Caption explaining the image")
```

Images link to their original full-size files. See [media provenance](assets/media/README.md). The builder rejects missing media and unfinished screenshot markers.

### Callouts

```text
::: warning Name the FSM
A blank name is valid only when the target has exactly one FSM.
:::
```

Available kinds: `note`, `tip`, and `warning`.

### Cards and Flows

```text
:::cards
- ↔ | Title | Short description | getting-started.md
:::

:::flow
- 01 | First step | What happens.
- 02 | Next step | What happens next.
:::
```

Card titles are visual labels, not article headings. Use H2/H3 headings for the page table of contents.

## Preview and Verify

```bash
python -m http.server 8086 --bind 127.0.0.1
```

Open [the local preview](http://127.0.0.1:8086/). Review desktop/mobile layouts, both themes, page filtering (`/` shortcut), keyboard navigation, mobile dismissal, copy buttons, section anchors, and wide-table scrolling.

`verify.py` checks generated freshness, page count, local links and anchors, duplicate IDs, media, required metadata, and unfinished content. Unit tests cover parser behavior. GitHub Actions runs these checks on pushes and pull requests.

## Publishing

The public repository is `Skyward-Games/PlayMaker-Integration-For-GC2-Documentation`. GitHub Pages serves branch `main`, folder `/`, matching the companion documentation sites. Generated HTML is committed, so Pages does not need Python to build the site. `.nojekyll` disables Jekyll processing.

After validation, commit and push the source, generated pages, assets, and tools together. Confirm the Pages deployment and representative live pages. No Unity package build or GitHub Release is required for a documentation update.

## Content Accuracy

This refresh checks claims against the plugin implementation and copies historical release notes through v1.1.3. It distinguishes qualified versions from later focused test results. Release validation numbers are historical records, not tests rerun by this documentation project.

The current scene 05/06 configuration gaps are documented in Examples and Compatibility. Plugin code, Unity scenes, and the companion documentation repositories are outside this repository's scope.

© Skyward Games.
