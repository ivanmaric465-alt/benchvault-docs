// Visual pass over the built site. Writes _shots/ (gitignored).
//
// Requires the Playwright install in ../eln_refactor/frontend. This repo has
// no node_modules of its own -- Playwright is imported directly via a
// relative ESM specifier that resolves into the sibling repo's install.
// (NODE_PATH does not work here: it is not honored for ESM import
// resolution. See README.md for the full story.)
import { chromium } from '../eln_refactor/frontend/node_modules/playwright/index.mjs'
import { mkdirSync } from 'node:fs'
import { createServer } from 'node:http'
import { readFile } from 'node:fs/promises'
import { extname, join, normalize } from 'node:path'

const ROOT = process.cwd()
const PORT = 8099
const PAGES = ['index', 'INSTALL', 'USER_GUIDE', 'ADMIN_GUIDE',
               'DOCKER_DEPLOY_GUIDE', 'CHANGELOG']
const SIZES = { desktop: { width: 1440, height: 900 },
                mobile: { width: 390, height: 844 } }
const TYPES = { '.html': 'text/html', '.css': 'text/css', '.png': 'image/png' }

const server = createServer(async (req, res) => {
  const rel = normalize(decodeURI(req.url.split('?')[0])).replace(/^(\.\.[/\\])+/, '')
  const file = join(ROOT, rel === '/' ? 'index.html' : rel)
  try {
    const body = await readFile(file)
    res.writeHead(200, { 'Content-Type': TYPES[extname(file)] ?? 'application/octet-stream' })
    res.end(body)
  } catch {
    res.writeHead(404).end('not found')
  }
})

await new Promise((r) => server.listen(PORT, r))
mkdirSync('_shots', { recursive: true })

const browser = await chromium.launch()
for (const [label, viewport] of Object.entries(SIZES)) {
  const page = await browser.newPage({ viewport })
  // The landing page reveals its sections (.reveal -> .in) via
  // IntersectionObserver as a real user scrolls. Playwright's full-page
  // screenshot renders the whole page in one composited pass without
  // dispatching real scroll events, so those sections would otherwise be
  // captured mid-animation at opacity: 0 -- a blank page, not a rendering
  // bug. The site's own CSS already gates that animation behind
  // `@media (prefers-reduced-motion: no-preference)`, so emulating reduced
  // motion here makes every section render at its resting (fully visible)
  // state, which is what we actually want to inspect.
  await page.emulateMedia({ reducedMotion: 'reduce' })
  for (const name of PAGES) {
    await page.goto(`http://localhost:${PORT}/${name}.html`,
                    { waitUntil: 'networkidle' })
    // Fail loudly rather than shipping a page that scrolls sideways.
    const overflow = await page.evaluate(
      () => document.documentElement.scrollWidth > window.innerWidth + 1
    )
    if (overflow) throw new Error(`${name}.html overflows horizontally at ${label}`)
    await page.screenshot({ path: `_shots/${label}-${name}.png`, fullPage: true })
    console.log(`captured ${label}-${name}`)
  }
  await page.close()
}
await browser.close()
server.close()
