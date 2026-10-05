# مول الدكة · MALL AL DIKKA

A static, mobile-first Arabic QR menu. No backend or production dependencies.

## Run

Run `python -m http.server 8080` in this folder, then open http://localhost:8080. Upload the static files to any static host. Do not upload `node_modules`, scripts, or audit contact sheets unless needed. No build is required.

## Configuration

Set `WHATSAPP_NUMBER` at the top of `js/app.js` to the café's international number, digits only (no plus sign). Until configured, ordering explains that WhatsApp is not available and never opens an invented number. No prices, sizes, promotions or availability have been fabricated.

## Files

- `index.html`: semantic Arabic RTL page and native accessible detail dialog.
- `css/style.css`: mobile-first responsive styling and reduced-motion support.
- `js/app.js`: search, filtering, favorites, quantity and WhatsApp messages.
- `data/menu-data.js`: structured drink records and Arabic category labels.
- `data/image-audit.json`: every source, selected poster and rejected duplicate appearances.
- `data/source-inventory.json`: source sizes and SHA256 hashes.
- `assets/source-images/`: untouched client originals.
- `assets/generated/thumbnails/`: 480 × 560 WebP drink crops.
- `assets/generated/logo.webp`: resized official logo, not a replacement design.
- `assets/generated/audit/`: review contact sheets and QA previews; not needed in deployment.

## Content audit

All 148 images were visually reviewed in indexed contact sheets. Multi-drink posters were split into individual products. Equivalent named recipes and repeated copies were grouped, preferring clear standalone posters. Original files were preserved. A V60 bean-origin guide is reference-only. Different recipes remain distinct. Ingredient lists are deliberately partial: only visible title ingredients and explicitly verified recipe lists are recorded. Unknown ingredient presence is `null`, not an assertion of absence. These posters establish menu candidates; confirm recipes with the café before service. Original recipe posters may retain supplier branding, while the website identity is exclusively Mall Al Dikka.

## Edit the menu

Add a record in `data/menu-data.js` with a unique `id`, `name`, category key, ingredient array, thumbnail `image` and original `source`. Copy its image into the assets folder. Delete its record to remove a drink. Categories and counts derive automatically from the remaining records. Empty categories do not appear. Keep audit records in sync when changing source selections.

The reproducible source mapping and crop rules live in `scripts/build_menu.py`. Running it regenerates menu data and thumbnails and overwrites manual menu edits. Python with Pillow is needed only for asset generation: `python -m pip install Pillow`, then `python scripts/build_menu.py`. `scripts/audit.py` recreates the indexed source inventory and contact sheets.

## Verification

Development-only browser QA: `npm install`, `npx playwright install chromium`, start the local server above, then `npm test`. It checks seven screen widths, local assets, duplicate IDs, search, categories, empty results, favorites, detail opening/closing, quantity minimum, and WhatsApp URL encoding. Favorites persist locally; storage failure does not block browsing.

## Photographic framing

`scripts/image_crops.py` contains individually reviewed photographic bounds for every selected source and each product within collection posters. Generated 480 × 560 thumbnails contain the selected photograph on a cream canvas without stretching. Cards and detail views also use `object-fit: contain`, so the browser does not crop the photograph again. Some collection images have limited original resolution; cropping does not create new photographic detail.

Open `image-review.html` locally to review all 202 photographs and click through to their untouched source. `data/image-quality-report.json` records crop sizes and small source images. Regenerate it with `python scripts/image_quality.py`. Run `node scripts/image_qa.cjs` against the local server to verify that all menu images decode successfully.

## Cup branding

The first 30 approved menu photos stay exactly as recorded in `data/retained-first-30-images.json`. Another 108 photographs use their original crop with the official Mall Al Dikka logo positioned over the old cup branding. Each photograph has reviewed percentage bounds in `data/logo-overlay-positions.json`, including the previous emblem and caption. `brandOverlay` and `brandOverlayBox` control rendering in the cards, detail sheet and review gallery. One previously selected image has no cup logo and is excluded. No new image generation is needed. All other photographs remain unchanged. Original sources and earlier generated variants are preserved.

`python scripts/apply_branded.py` preserves the first 30 and applies reviewed positions to IDs recorded in `data/remaining-brand-jobs.json`. Rebuilding with `scripts/build_menu.py` preserves the same selection. `python scripts/verify_image_scope.py` verifies this rule; `node scripts/overlay_qa.cjs` checks card/detail overlays and their removal when switching to an unbranded photo. Earlier generated variants and their prompts in `data/branded-image-manifest.json` remain archived; they are not used for these 108 overlays.

## Refined photo framing

51 original photographs with recipe margins use tighter reviewed crops in assets/generated/framed/. scripts/clean_photo_framing.py retains the visible vessel and remaps the cup-logo overlay to the new canvas. data/framed-image-manifest.json preserves crop bounds and logo positions. First 30 approved photos remain unchanged. These crops improve framing but do not invent detail missing in the original source.
