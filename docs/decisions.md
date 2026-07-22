# Design & Architecture Decisions

**Project:** Md Adnan Umar — GitHub Profile  
**Last Updated:** 2026-07-22

---

## DEC-01 — SMIL for all animations

**Decision:** Use only SMIL (`<animate>`, `<animateTransform>`) for SVG animations.  
**Alternatives considered:** CSS animations (`@keyframes`), JavaScript (`requestAnimationFrame`).  
**Reason:** GitHub's Camo CDN proxy strips `<style>` tags and all `<script>` tags from SVGs during rendering. SMIL is the only animation mechanism that survives the sanitisation pipeline. This is a hard constraint, not a preference.

---

## DEC-02 — Base64 embedded photo

**Decision:** Embed the circular headshot as a `data:image/png;base64,…` URI directly inside the SVG `<image href="…">` element.  
**Alternatives considered:** Relative path (`./pic-circle.png`), raw GitHub URL (`https://raw.githubusercontent.com/…`).  
**Reason:** GitHub's Camo proxy intercepts all external URL references in SVGs. A relative path fails because GitHub renders the SVG in an isolated context, not relative to the repository root. A raw GitHub URL works in some browsers but triggers a second HTTP request that the proxy may block or delay. Base64 embedding is the only approach that is guaranteed to work in GitHub's renderer with zero additional requests.  
**Trade-off:** Adds ~114 KB to each SVG file. Acceptable given GitHub's image display limit is 250 KB and the asset renders inline.

---

## DEC-03 — System monospace font stack

**Decision:** Use `ui-monospace, SFMono-Regular, Menlo, Consolas, monospace` for all SVG text.  
**Alternatives considered:** Loading a specific web font (JetBrains Mono, Fira Code) via `@font-face`.  
**Reason:** SVG `<style>` tags are stripped by GitHub. Web fonts loaded via `@font-face` inside `<style>` are therefore unavailable. The system monospace stack resolves to native monospace fonts on every platform (SF Mono on macOS, Consolas on Windows, DejaVu/Liberation on Linux), which is precisely the right aesthetic for a terminal card. No loading delay, no layout shift.

---

## DEC-04 — rembg for background removal

**Decision:** Use `rembg` (u2net model) for headshot background removal instead of OpenCV colour masking.  
**Alternatives considered:** OpenCV HSV colour range masking, manual Photoshop masking.  
**Reason:** The initial implementation used OpenCV HSV masking. This worked adequately for the uniform light-blue studio background but produced uneven edges around hair and produced green fringing around the subject boundary. rembg's u2net neural model handles complex edges (hair strands, shoulder edges) with significantly higher quality. The 176 MB model download is a one-time cost cached in `~/.u2net/`.

---

## DEC-05 — Split-panel hero layout

**Decision:** Left panel for photo + identity, right panel for terminal/code.  
**Alternatives considered:** Single full-width layout, photo on right, full-bleed ASCII art background.  
**Reason:** The split panel creates a clear visual hierarchy: identity (who I am) on the left, technical signal (what I build) on the right. This maps to natural left-to-right reading order. A full-width layout spreads elements too thin at 1180px. Photo-on-right is less natural since the eye starts at the top-left. The Megha Mittal reference profile validated this layout pattern.

---

## DEC-06 — Three-accent colour palette

**Decision:** Violet (`#7C3AED`) / Cyan (`#22D3EE`) / Emerald (`#10B981`) for dark; Blue / Cyan / Green for light.  
**Alternatives considered:** Two-colour palette, four or more colours, single accent.  
**Reason:** Two colours felt flat for a terminal aesthetic. Four or more colours introduced visual noise and made skill pills harder to distinguish. Three colours allow three distinct pill variants, three distinct info categories, and a gradient that cycles through all three — enough variety to create depth without chaos.

---

## DEC-07 — Standalone `make_info_card.py`

**Decision:** Keep `make_info_card.py` as a standalone script with a fallback to extract base64 from existing `info-card.svg`.  
**Alternatives considered:** Import shared builder from `_build_svgs.py`.  
**Reason:** `_build_svgs.py` is a build-time script that reads `pic-b64.txt` and generates all three hero assets at once. `make_info_card.py` needs to be runnable independently to regenerate only the info card when profile data changes (new skill added, role update, etc.) without rebuilding the 280 KB of hero SVGs. Keeping them separate honours the Single Responsibility Principle. The fallback ensures it works even without `scripts/pic-b64.txt`.

---

## DEC-08 — Daily contribution refresh

**Decision:** Refresh contribution data daily at 06:00 UTC via GitHub Actions.  
**Alternatives considered:** Refresh on every push, use GitHub GraphQL API with token.  
**Reason:** Refreshing on every push would be wasteful — contribution data only changes once per day. The GraphQL API requires storing a PAT as a secret, which adds setup complexity for anyone forking this profile. The scraping approach reads the same public HTML GitHub serves to anonymous visitors — no token required, no secret to manage.

---

## DEC-09 — `[skip ci]` in automated commits

**Decision:** All commits made by the `update-profile.yml` workflow include `[skip ci]` in the message.  
**Reason:** Without this, every workflow commit triggers the workflow again, creating an infinite loop. `[skip ci]` is a GitHub Actions convention that prevents the new commit from triggering additional workflow runs.

---

## DEC-10 — `pic-b64.txt` not committed

**Decision:** `scripts/pic-b64.txt` is listed in `.gitignore` and never committed.  
**Reason:** The base64 string is ~114 KB of pure text. Committing it would bloat the repository history permanently (Git stores the full content of every version of every file). The file is generated/extracted locally and consumed locally during the SVG build step. `make_info_card.py` falls back to extracting the base64 directly from the existing `info-card.svg` if `pic-b64.txt` is missing.

---

## DEC-11 — Static achievements instead of external trophy service

**Decision:** Replace `github-profile-trophy.vercel.app` with a static markdown achievements table.  
**Alternatives considered:** Continue using github-profile-trophy, use `github-readme-achievements` API.  
**Reason:** The trophy service is rate-limited, slow to render, and has experienced extended downtime. A static markdown table is instant, always renders, never breaks, and still communicates the same information. Profile achievements are now visible natively on GitHub profiles, making the trophy widget redundant.

---

## DEC-12 — Remove external visit counters

**Decision:** Remove `komarev.com/ghpvc/` and `visitcount.itsvg.in` badges from README.  
**Alternatives considered:** Keep one of the services, replace with self-hosted counter.  
**Reason:** Both services are external dependencies that can disappear, rate-limit, or break without warning. Profile view counts are not critical to the profile's function. A clean, fast-loading README without these external HTTP requests is more reliable and professional.
