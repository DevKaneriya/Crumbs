# Crumbs — Product Image Regeneration (Gemini Nano Banana)

## Original Problem Statement
Regenerate all Surili-branded product images in the Crumbs storefront (Django + Angular repo `DevKaneriya/Crumbs`) as Crumbs-branded, Diwali-styled photorealistic product shots using Gemini Nano Banana via `emergentintegrations`, using `/app/frontend/src/assets/logo.png` as the brand reference, and overwrite the existing `.webp` files in `/app/frontend/src/assets/products/**` (and mirror to `/app/frontend/public/assets/products/**`). Use free Universal Key credits, batch-by-batch.

## Architecture / Setup
- Repo cloned from `https://github.com/DevKaneriya/Crumbs.git` into `/app`
- Backend: Django (SQLite `db.sqlite3` — 41 products across `catalog_product`)
- Frontend: Angular (assets in `frontend/src/assets/products/**` and mirrored `frontend/public/assets/products/**`)
- Image gen: Gemini `gemini-3.1-flash-image-preview` via `emergentintegrations` (Universal Key)
- Env: `/app/backend/.env` has `EMERGENT_LLM_KEY`

## Deliverables in this session
- Built catalog JSON from SQLite → `/app/backend/complete_surili_catalog.json` (41 products, 96 images)
- Saved user-uploaded richer catalog → `/app/backend/complete_surili_catalog_user_uploaded.json`
- Image gen script → `/app/scripts/generate_crumbs_images.py`
  - Expanded `PRODUCT_HINTS` to cover all 41 catalog products (added dilkhush, gujarati, dhana-dal, classic-pan-supari-fusion, sweet-caramelized-elaichi-bliss, saffron-pistachio-symphony, royal-anardana-mix, spicy-minty-saunf-elixir, tangy-imli-goli-temptation, spicy-adrak-dhaniya-crunch)
  - Added CLI flags `--start N --end M` for batch runs
  - Writes to both `frontend/src/assets/` and `frontend/public/assets/`
- Resume artifacts:
  - `/app/scripts/failed_images_to_regenerate.txt` — 22 relative paths still needing generation
  - `/app/scripts/failed_shorts.txt` — 16 unique product shorts to pass to the script

## Status (as of finish)
- **74 / 96 images regenerated** and mirrored to both `src` and `public` folders.
- **22 / 96 images still show the old Surili branding** (budget cap hit at ~$2.93).
- Quality of the 74 done: verified — CRUMBS wordmark, orange/yellow gradient label, navy cap, festive Diwali background with marigolds, diyas, and side bowls of contents. Style is consistent and on-brand.

## 16 products still needing re-run
honey-coated-mukhwas, jeera-goli-digestive, lemon-mint-refresher, magic-mint-mukhwas, mini-chocolate-coated-nuts, panchratna-churan, royal-pan-masala, sada-pan-mix, saffron-infused-mukhwas, saffron-pistachio-symphony, scented-chocolate-supari, sweet-caramelized-elaichi-bliss, traditional-katha-supari, traditional-mixed-seeds-mukhwas, wedding-return-gift-pack, zero-sugar-saunf-mix

## Resume command (after topping up Universal Key)
```
cd /app && python3 scripts/generate_crumbs_images.py $(cat scripts/failed_shorts.txt | tr '\n' ' ')
```
(This regenerates ALL variants of those 16 products — will overwrite the 20 already-good ones for those products with fresh takes, plus fill the missing 22. If you want strictly-only-missing, filter by the file list in `failed_images_to_regenerate.txt`.)

## Backlog / Next Actions
- P0: Top up Universal Key balance (+~$1) and re-run the 16 products above
- P1: Rebuild Angular frontend so new `public/assets/products/**` is bundled (`cd /app/frontend && ng build`)
- P2: Delete un-referenced old files if any (e.g. `sugar-free-digestive-mix.webp` vs `sugar-free-digestive-mukhwas.webp` — DB has both)
- P2: Consider running with `gemini-3-pro-image-preview` for hero shots only (higher quality, higher cost)
