# AGENTS.md

## What this repo is

A single-page landing site (**`index.html` + `assets/style.css`**, no framework, no JS) built from the design mockup **`Main.psd`** (1920×6042, render: `Main-preview.png`), plus a Playwright audit suite (performance / SEO / a11y / screenshots / Lighthouse) that tests it at **http://localhost:3333** (live-server).

Palette: green `#4caf50` / `#8bc34a`, hero `#000`, tiles `#414141`, CTA `#282828`, footer `#262626`, light sections `#fafafa` / `#f7f7f7`. Content language: English; test titles: Ukrainian.

## Commands

```bash
npm install                # package-lock.json exists; needed only after dep changes
npm run dev                # live-server on port 3333 (--no-browser)
npm test                   # playwright test (all 5 browsers)
npm run test:ui            # playwright test --ui
npm run test:report        # open HTML report (playwright-report/)
npx tsc --noEmit           # the only typecheck — no lint/format scripts exist
```

Focused runs (there is no script for these):

```bash
npx playwright test performance --project=chromium --retries=1   # single file
npx playwright test --project=chromium                            # Chromium only (fastest)
npx playwright test --update-snapshots                            # refresh visual baselines
npx playwright test -g "Title tag"                                # single test by name
```

## Required order: start the server yourself

`playwright.config.ts` has the `webServer` block **commented out** — Playwright will not start live-server for you. Run `npm run dev` in a separate terminal first, otherwise every test fails on `page.goto('/')`.

`BASE_URL` is defined once at the top of `playwright.config.ts` and feeds `use.baseURL`. Change it there to point tests at another site; never hardcode hostnames in specs.

## Test architecture gotchas

- **The first `a[href]` in DOM must fire a real HTTP request when clicked.** `performance.spec.ts` "Click handler non-blocking" clicks `a[href]` `.first()` and awaits `waitForRequest`. `mailto:` and `#hash` first-links pass on Chromium but **time out on Firefox**. Currently the first link is the topbar social (external https) — keep any real HTTP link ahead of `mailto:`/anchors.
- **Full-page screenshot budget is 14s (`actionTimeout`, raised from 10s)** on Mobile Safari (iPhone 12, deviceScaleFactor 3 → ~5760px-wide, ~84MP capture). Cost is dominated by **pixels, not paint**: a blank page of the same height took ~7.9s at height 5214 (WebKit CPU raster on a 4-core box, no GPU) — so page height is the main lever: current height ≈ 4673 → ~6s. Blank-page floor ≈ 1.5ms per CSS px of height; if you add sections, keep total height ≲ 5000 and verify with `npx playwright test --project="Mobile Safari" -g "Desktop screenshot"` (also watch CPU contention: the machine had ~65% background load when timings spiked). Heavy paint (repeating gradients, large blurred box-shadows) adds on top — keep background/shadow CSS flat.
- **`perf` fixture only exists in `performance.spec.ts`.** That file re-exports `base.extend<{ perf: PerfHelpers }>`; all other specs import plain `test` from `@playwright/test`. To use `perf.getTTFB()` etc. elsewhere, replicate that `extend` block. Shared helper class: `tests/helpers/perf.ts`.
- **Chromium-only tests self-skip**: Lighthouse (CDP), HSTS, and Early Hints call `test.skip(browserName !== 'chromium')`. Skips on other browsers are expected (21 skipped in a green run).
- **Many assertions are intentionally lenient** — compression, cache headers, resource hints, service worker, bfcache mostly `console.log` a warning instead of failing (dev-server limitations). Do not "tighten" them without being asked; several tests exist purely to print summary reports.
- **Visual regression**: baselines live in `tests/screenshots.spec.ts-snapshots/` (10 files, one per browser project). After any visual/layout change run `npx playwright test --update-snapshots` and then a clean `npm test` to verify.
- **Per-file overrides**: accessibility, seo, screenshots set `test.describe.configure({ timeout: 10000–15000, retries: 0 })`, overriding the global 30s / 1 retry — under parallel load these can flake (e.g. `page.goto` blowing a 10s budget); a green run must be checked as a whole.
- Projects: chromium, firefox, webkit, Mobile Chrome (Pixel 5), Mobile Safari (iPhone 12). Chromium is the priority browser.

## Conventions

- **Markup is self-contained**: inline SVG icons, CSS-drawn placeholders (zero `<img>`, zero external requests) — keep it that way; adding external resources risks the `networkidle` / LCP tests.
- **New tests and comments are written in Ukrainian** (per `spec.md`: `language: uk-UA`). Match existing test titles' style (emoji + Ukrainian description).
- `spec.md` is the generator spec that produced these tests, including fail thresholds (TTFB < 800ms, redirect chain ≤ 1, cookies < 4KB) and the canonical run command. Trust `playwright.config.ts` over it where they disagree.
- `tsconfig.json` only includes `tests/**/*` and `playwright.config.ts` — nothing else is typechecked (page assets are untyped static files).

## Tooling notes

- `opencode.jsonc` enables a local `chrome-devtools-mcp` server for live browser inspection; use it to debug the page under test instead of guessing DOM structure.
- **Production**: the site deploys to **https://photon-studio-opencode.vercel.app/** (Vercel project `photon-studio-opencode`, linked via `.vercel/project.json`). Canonical / `og:url` / JSON-LD `url` in `index.html` and `<loc>` in `sitemap.xml` must point at that origin — never `localhost` (tests run against localhost but do not assert on the canonical value). `npm run deploy` → `vercel --prod` (only run when explicitly asked).
