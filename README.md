# Photon Studio Landing — готова збірка під верстку PSD-макетів

Універсальна збірка: **PSD-макет → статичний лендінг** (HTML + CSS, без фреймворків і JS) з повним набором перевірок (Playwright: performance / SEO / a11y / візуальні тести / Lighthouse) і деплоєм на Vercel.

Кинув новий `.psd` у папку → відрендерив прев'ю → віддав опенкоду → він верстає все сам: розмітку, стилі, SEO, проходить тести.

- **Продакшен:** https://photon-studio-opencode.vercel.app/
- **Приклад макета:** `Main.psd` (1920×6042), прев'ю: `preview/Main-preview.png`

---

## 1. Що встановити

| Що | Навіщо | Як |
|---|---|---|
| **Node.js 20+** | живий сервер, тести, деплой | https://nodejs.org |
| **Python 3.11+** | рендер PSD у PNG | вже є (3.14) |
| **psd-tools** | Python-бібліотека для читання PSD | `pip install psd-tools` |
| **Playwright + браузери** | тести (Chromium, Firefox, WebKit) | `npm install` і `npx playwright install` |
| **opencode** | AI-агент, який верстає | https://opencode.ai або `npm i -g opencode-ai` |
| **Vercel CLI** | деплой (опційно) | `npm i -g vercel` → `vercel login` |
| **Photon Studio** (опційно) | безкоштовний Photoshop-альтернатива — відкрити PSD локально з шарами | https://tenzen.studio/photon/ (macOS / Windows / Linux, безкоштовно, офлайн) |

Один раз на проєкт:

```bash
npm install
npx playwright install
```

---

## 2. Як запустити

```bash
npm run dev        # live-server на http://localhost:3333
npm test           # всі тести (5 браузерів, ~294 тести, ~5 хв)
npm run test:report  # відкрити HTML-звіт
npm run deploy     # деплой на Vercel (vercel --prod)
```

**Важливо:** `webServer` у `playwright.config.ts` вимкнений — запускай `npm run dev` в окремому терміналі **перед** `npm test`, інакше всі тести впадуть на `page.goto('/')`.

Швидкі запуски:

```bash
npx playwright test --project=chromium              # тільки Chromium (~1.5 хв)
npx playwright test performance --project=chromium  # один файл
npx playwright test -g "Title tag"                  # один тест
npx playwright test --update-snapshots              # оновити візуальні базлайни
```

---

## 3. Як верстати НОВИЙ макет (основний сценарій)

### Крок 1 — кинь PSD у корінь проєкту

Наприклад `Landing.psd`.

### Крок 2 — відрендер прев'ю + структура шарів

```bash
python tools/render_psd.py Landing.psd
```

Виведе:
- розмір полотна і колірний режим;
- **дерево верхньорівневих шарів = секції макета** (Head, About, Service, …) з bbox-координатами;
- збереже `preview/Landing-preview.png` — повнокольорове прев'ю для порівняння.

### Крок 3 — відкрий у Photon Studio (за бажанням)

[Photon Studio](https://tenzen.studio/photon/) — безкоштовний локальний Photoshop-альтернатива: відкриває PSD зі шарами, масками, текстом і горячими клавішами як у PS, зберігає назад у PSD/PSB, працює офлайн. Завантаження: https://tenzen.studio/download/ (Windows x64/ARM64, macOS, Linux; також [Microsoft Store](https://apps.microsoft.com/detail/9PLD16DV387N)).

### Крок 4 — дай опенкоду промпт

Відкрий opencode **в папці проєкту** (`opencode`) і встав:

```
У папку кинуто макет Landing.psd. Відрендери його:
python tools/render_psd.py Landing.psd

Дивись preview/Landing-preview.png і bbox шарів як референс. Переверстати index.html +
assets/style.css під цей макет повністю, секція за секцією (усі верхньорівневі
шари з PSD — це секції сторінки, їх порядок зверху вниз = порядок секцій).

Правила збірки:
- чистий HTML + CSS, без фреймворків і без JS;
- self-contained розмітка: жодного <img> і жодних зовнішніх запитів —
  іконки inline SVG, картинки з макета — CSS-плейсхолдери;
- палітра з макета — CSS-змінні у assets/style.css;
- семантика, alt/aria, контраст ≥ 4.5 (Lighthouse a11y має бути 100);
- SEO: title, description, canonical + og:url → https://photon-studio-opencode.vercel.app/,
  оновити sitemap.xml;
- тексти сторінки — англійською, назви тестів і коментарі в tests/ — українською.

Після верстки: запусти npm run dev на :3333, перевір сторінку через
chrome-devtools MCP (скріншоти на 1920), потім npx playwright test --update-snapshots
і чистий npm test — має бути 0 failed. Візуальні базлайни оновлюй тільки після
того, як сторінка виглядає правильно.
```

---

## 4. Скіли для opencode

### Вже стоять у цьому проєкті

| Скіл | Звідки | Навіщо |
|---|---|---|
| `modern-web-guidance` | GoogleChrome/modern-web-guidance | **обов'язковий** для HTML/CSS-завдань: сучасні CSS (container queries, `:has()`, fluid type), a11y, Core Web Vitals |
| `chrome-extensions` | той самий репозиторій | розробка Chrome-розширень (у цьому проєкті не потрібен) |

Лежать у `.agents/skills/`, хеші у `skills-lock.json`. Оновити:

```bash
npx skills add GoogleChrome/modern-web-guidance -y --copy
```

### Поставити додаткові скіли

Формат [Agent Skills](https://skills.sh/) — опенкод підхоплює їх автоматично:

```bash
npx skills add GoogleChrome/modern-web-guidance   # гугл: CSS/HTML/a11y/performance
npx skills add photon-hq/skills --skill spectrum   # Photon SDK (iMessage/WhatsApp/terminal)
npx skills add photon-hq/skills --skill photon-cli # photon CLI (dashboard/лінії/білінг)
npx skills find <запит>                            # пошук скілів
npx skills list                                    # що встановлено
npx skills update                                  # оновити всі
```

Скіли `photon-hq/skills` (imessage, spectrum, photon-cli, chat-adapter-imessage, buildspace-ci-cd) — це для роботи з Photon SDK (photon.codes): месенджери, CLI, CI/CD. **Не плутати з Photon Studio** (tenzen.studio) — це Photoshop-альтернатива, у неї свої вбудовані skills/CLI/MCP (Settings → integrations у застосунку).

### Корисні скіли OpenCode

- `find-skills` — знайти і встановити скіл під задачу;
- `opencode` — питання по самому OpenCode (agent, tools, MCP, themes);
- `report` — якщо знайшов баг у OpenCode, оформити issue.

---

## 5. Тести (Playwright)

Усього ~294 тести, 5 проєктів: chromium, firefox, webkit, Mobile Chrome (Pixel 5), Mobile Safari (iPhone 12). Chromium — пріоритетний.

| Файл | Що перевіряє |
|---|---|
| `tests/performance.spec.ts` | TTFB < 800ms, LCP/CLS/FCP, cache, стиснення, bfcache, звіт |
| `tests/seo.spec.ts` | title, description, canonical, h1, OG, sitemap/robots, JSON-LD |
| `tests/accessibility.spec.ts` | aria, alt, контраст, headings order |
| `tests/screenshots.spec.ts` | візуальні базлайни (`tests/screenshots.spec.ts-snapshots/`) |
| `tests/lighthouse.spec.ts` | Lighthouse (Chromium/CDP) |

Головні гетчі (детальніше — в `AGENTS.md`):

- **перший `a[href]` у DOM має давати реальний HTTP-запит** (Firefox таймить на `mailto:`/якірцях);
- **бюджет повноекранного скріншота — 14s** (`actionTimeout`): WebKit на dsf=3 растеризує ~84MP на CPU, тримай висоту сторінки ≲ 5000px;
- після будь-якої зміни візуалу — `npx playwright test --update-snapshots`, потім чистий `npm test`;
- Lighthouse/HSTS/Early Hints самі скипаються поза Chromium (21 skip у зеленому прогоні — норма).

---

## 6. Структура проєкту

```
index.html              розмітка (усі секції макета)
assets/style.css        стилі (CSS-змінні з палітри макета)
robots.txt, sitemap.xml SEO
Main.psd                вихідний макет
preview/Main-preview.png  рендер макета (python tools/render_psd.py)
tools/render_psd.py     рендер PSD → PNG + дерево шарів
tests/                  Playwright-тести (назви українською)
playwright.config.ts    5 браузерів, baseURL http://localhost:3333
opencode.jsonc          chrome-devtools MCP для живої перевірки в браузері
.agents/skills/         скіли проєкту (modern-web-guidance)
AGENTS.md               гетчі збірки для агента
spec.md                 вихідна специфікація тестів
```

---

## 7. Деплой

```bash
npm run deploy   # vercel --prod
```

Продакшен-домен: **https://photon-studio-opencode.vercel.app/** — canonical / `og:url` / JSON-LD `url` в `index.html` і `<loc>` у `sitemap.xml` мають вказувати на нього, ніколи на `localhost`.

---

## Ліцензія

ISC
