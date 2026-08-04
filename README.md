# benchvault-docs

The documentation site for [BenchVault](https://github.com/ivanmaric465-alt/benchvault),
published at <https://ivanmaric465-alt.github.io/benchvault-docs/>.

**This site is generated. Do not hand-edit anything at the repository root.**
Everything there — `index.html`, the five guide pages, the redirect stubs,
`site.css`, `images/` — is produced by `build.py` and overwritten on every run.

Hand-authored sources live in `src/`:

| File | What it is |
|---|---|
| `src/index.html` | The landing page |
| `src/layout.html` | The shell wrapped around each generated guide |
| `src/site.css` | Design tokens and all styling |
| `src/app_icon.png` | The brand mark |

The five guides themselves are **not** in this repository. They are
`docs/*.md` in the application repository, and are converted on each build, so
there is exactly one copy of every sentence.

## Rebuilding after a release

```bash
pip install -r requirements.txt
python build.py --source ../eln_refactor
python check.py --source ../eln_refactor
python -m pytest -q
git add -A && git commit -m "Sync docs for BenchVault vX.Y.Z" && git push
```

`--source` points at your `benchvault` checkout. The version shown across the
site is read from that checkout's `utils/version.py`, so it can never drift.

`check.py` fails the build on a broken link, a stale version number, or a
mention of a retired product (PyQt6, Flutter, the Android app, Whisper). The
site sat four versions out of date because nothing checked; that is what these
rules are for.

## Previewing

Any static server works:

```bash
python -m http.server 8080
```

For a visual pass at both breakpoints:

```bash
node capture.mjs      # writes _shots/ (gitignored)
```

This repo has no `node_modules` of its own — Playwright is not a dependency
here. `capture.mjs` imports it directly from the sibling `benchvault`
checkout's frontend install:

```js
import { chromium } from '../eln_refactor/frontend/node_modules/playwright/index.mjs'
```

That relative ESM specifier resolves normally as long as `benchvault-docs`
and `benchvault` (`eln_refactor`) are checked out next to each other, e.g.
`D:\CODE\benchvault-docs` and `D:\CODE\eln_refactor`. If your layout differs,
adjust the path in `capture.mjs` (or point it at any other local Playwright
install — `require('playwright').chromium` would do too).

Two things that do **not** work, in case you're tempted:
- `NODE_PATH=../eln_refactor/frontend/node_modules node capture.mjs` —
  `NODE_PATH` is a CommonJS-era mechanism; Node's ESM resolver ignores it
  entirely, so a bare `import { chromium } from 'playwright'` still fails
  to resolve even with `NODE_PATH` set.
- Running the script with its working directory set to
  `../eln_refactor/frontend` — `capture.mjs` uses `process.cwd()` as both
  the static file root it serves and the place it writes `_shots/`, so
  changing `cwd` would serve the wrong site and write the captures into the
  wrong repo.

Playwright's browser binaries (Chromium etc.) are cached at the OS level
(e.g. `~/AppData/Local/ms-playwright` on Windows), not inside
`node_modules`, so they resolve correctly regardless of which repo the
import path points through.
