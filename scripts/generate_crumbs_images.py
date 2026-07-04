"""
Generate Crumbs product images using Gemini Nano Banana.
- Reads complete_surili_catalog.json
- For each image path referenced, generates a festive/Diwali-styled product shot
  showing a jar labeled "CRUMBS" with the appropriate mukhwas/contents.
- Uses the Crumbs logo as a reference image so branding stays consistent.
- Saves output as .webp using Pillow (Gemini returns PNG bytes).
"""

import asyncio
import os
import sys
import json
import base64
import io
from pathlib import Path
from dotenv import load_dotenv
from PIL import Image
from emergentintegrations.llm.chat import LlmChat, UserMessage, ImageContent

load_dotenv("/app/backend/.env")

API_KEY = os.getenv("EMERGENT_LLM_KEY")
MODEL_ID = "gemini-3.1-flash-image-preview"
CATALOG_PATH = "/app/backend/complete_surili_catalog.json"
LOGO_PATH = "/app/frontend/src/assets/logo.png"
ASSETS_ROOT_SRC = "/app/frontend/src"
ASSETS_ROOT_PUB = "/app/frontend/public"

# ---- Per-product styling hints (visual contents inside the jar / bowl) -----
PRODUCT_HINTS = {
    "sugar-free-digestive-mukhwas":   "small mixed digestive seeds (fennel, sesame, ajwain), soft greenish-brown tones",
    "sugar-free-digestive-mix":       "small mixed digestive seeds (fennel, sesame, ajwain), soft greenish-brown tones",
    "digestive-mukhwas":              "small mixed digestive seeds (fennel, sesame, ajwain), soft greenish-brown tones",
    "dilkhush-mukhwas":               "colorful sweet dilkhush mukhwas with dried rose petals, coconut and sugar crystals",
    "gujarati":                       "traditional Gujarati mukhwas mix with fennel, sesame, and colored sugar bits",
    "dhana-dal-special-mukhwas":      "roasted split coriander (dhana dal) seeds, pale yellow-green split lentils",
    "zero-sugar-saunf-mix":           "bright green fennel seeds (saunf) mix",
    "diabetic-friendly-ajwain-crunch":"roasted ajwain (carom) seeds, brownish-green crunchy mix",
    "royal-pan-masala":               "colorful pan masala mix with multi-color sugar coated fennel and rose petals",
    "magic-mint-mukhwas":             "bright mint-green coated fennel mukhwas with white sugar bits",
    "golden-elaichi-delight":         "golden cardamom (elaichi) coated seeds shimmering golden-yellow",
    "traditional-mixed-seeds-mukhwas":"traditional mixed seeds mukhwas, earthy colors with sesame and fennel",
    "rose-petal-special":             "pink rose petal mukhwas with dried rose petals and sugar crystals",
    "saffron-infused-mukhwas":        "deep saffron orange mukhwas with strands of saffron",
    "amchur-imli-churan":             "dark brown tangy amchur-imli churan powder/granules",
    "jeera-goli-digestive":           "dark brown jeera goli digestive balls",
    "panchratna-churan":              "multi-color (5 jewel) churan granules - red, brown, green, yellow",
    "premium-meetha-supari":          "sweet shredded betel-nut (supari) pieces, light brown",
    "scented-chocolate-supari":       "chocolate brown sweet supari pieces glossy",
    "traditional-katha-supari":       "traditional katha-supari, deep reddish-brown nut pieces",
    "special-meetha-pan":             "fresh green pan leaf rolled mouth freshener, green coconut mix",
    "sada-pan-mix":                   "classic green pan mix with shredded coconut and fennel",
    "chocolate-pan-fusion":           "chocolate brown sweet pan fusion granules",
    "classic-pan-supari-fusion":      "classic pan supari fusion with green coconut and betel-nut pieces",
    "colorful-sugar-balls":           "tiny rainbow colored sugar-coated fennel candy balls",
    "mini-chocolate-coated-nuts":     "mini chocolate-coated nuts (cashew, almond) glossy brown",
    "rainbow-confectionery-mix":      "rainbow confectionery mix - bright red, yellow, blue, pink candies",
    "sweet-caramelized-elaichi-bliss":"sweet caramelized cardamom pieces, golden-amber shiny",
    "premium-gift-hamper":            "premium gift hamper with assorted mukhwas in small bowls around the jar",
    "diwali-special-combo":           "diwali special - assortment of golden, red and green mukhwas around the jar with diyas",
    "wedding-return-gift-pack":       "wedding return-gift styled with marigold flowers and pastel mukhwas",
    "saffron-pistachio-symphony":     "saffron and pistachio mukhwas mix - orange saffron strands and green pistachio bits",
    "honey-coated-mukhwas":           "honey-coated fennel mukhwas, glossy golden-amber",
    "cinnamon-spice-mix":             "cinnamon spice mukhwas, deep reddish-brown with cinnamon sticks",
    "lemon-mint-refresher":           "fresh lemon-mint green mukhwas with white sugar dots",
    "dry-fruit-delight":              "premium dry-fruit mix: cashew, almond, pistachio, raisins",
    "ayurvedic-digestive-mix":        "ayurvedic digestive mix, earthy brown-green herbal granules",
    "royal-anardana-mix":             "royal anardana (dried pomegranate seed) mix - dark red-brown tangy granules",
    "spicy-minty-saunf-elixir":       "spicy minty fennel (saunf) elixir - bright green fennel with mint flecks",
    "tangy-imli-goli-temptation":     "tangy tamarind (imli) goli balls, deep brown glossy candies",
    "spicy-adrak-dhaniya-crunch":     "spicy ginger-coriander crunchy mukhwas, brownish-green with white ginger bits",
}

# ---- Image variant styling -------------------------------------------------
def variant_style(filename: str) -> str:
    """Different camera/lighting/background for each variant of the same product."""
    f = filename.lower()
    if f.endswith("-hover.webp"):
        return (
            "Camera angle: slight close-up from a 30-degree side angle. "
            "Background: deep teal-green silk fabric with warm Edison-bulb string lights bokeh. "
            "Place a small open bowl of the contents tilted toward the camera with a few seeds spilled on the surface."
        )
    if f.endswith("-3.webp") or f.endswith("-4.webp") or f.endswith("-5.webp"):
        return (
            "Camera angle: top-down flat-lay shot. "
            "Background: dark rustic wood plank with a large oval wooden platter; the jar is laid horizontally "
            "with the contents arranged in an oval ring around it, marigold petals and a small clay diya in one corner."
        )
    # default / main shot
    return (
        "Camera angle: front-facing eye-level hero shot. "
        "Background: rich maroon silk drape with golden marigold flowers and lit clay diyas (oil lamps), "
        "soft warm festive bokeh. Place a small clay or wooden bowl of the contents next to the jar."
    )


BASE_PROMPT = """Create a high-end, photorealistic Indian festive product photograph of a single
glass mukhwas jar / bottle (similar shape to a typical mouth-freshener jar) with a printed wrap-around
paper label that prominently features the brand name **"CRUMBS"** in the exact bubbly rounded
orange wordmark style shown in the reference logo (orange #F07B24 + yellow #FFD12F accents,
small "crumb" cluster decoration to the upper-right of the word). The label also shows the product
name **"{display_name}"** in clean white sans-serif underneath the logo, on an orange-to-yellow
gradient band. The cap of the jar is dark navy-blue.

Inside the jar (visible through the glass) the contents are: **{contents}**.

{variant_style}

Overall mood: warm Diwali / festive Indian celebration, cinematic studio lighting,
golden hour warm tones, rich textures, very sharp focus on the jar, slight depth of field on background.
Square 1:1 aspect ratio, e-commerce product hero quality.

Strict rules:
- Brand text on the label must read exactly **CRUMBS** (no other brand name, no "Surili", no misspellings).
- Do not add any other floating text, watermarks, prices or badges.
- Only ONE jar in the frame.
- Do not include human hands or faces.
"""


def build_prompt(short_name: str, display_name: str, filename: str) -> str:
    contents = PRODUCT_HINTS.get(short_name, "premium Indian mukhwas mix")
    return BASE_PROMPT.format(
        display_name=display_name,
        contents=contents,
        variant_style=variant_style(filename),
    )


def png_bytes_to_webp(png_bytes: bytes, out_path: Path):
    img = Image.open(io.BytesIO(png_bytes)).convert("RGB")
    img.save(out_path, format="WEBP", quality=88, method=6)


async def generate_one(logo_b64: str, short_name: str, display_name: str, rel_path: str, sem: asyncio.Semaphore):
    out_src = Path(ASSETS_ROOT_SRC) / rel_path
    out_pub = Path(ASSETS_ROOT_PUB) / rel_path
    out_src.parent.mkdir(parents=True, exist_ok=True)
    out_pub.parent.mkdir(parents=True, exist_ok=True)

    filename = out_src.name
    prompt = build_prompt(short_name, display_name, filename)

    async with sem:
        try:
            chat = LlmChat(
                api_key=API_KEY,
                session_id=f"crumbs-{short_name}-{filename}",
                system_message="You are an expert Indian festive product photographer creating premium e-commerce shots.",
            )
            chat.with_model("gemini", MODEL_ID).with_params(modalities=["image", "text"])

            msg = UserMessage(
                text=prompt,
                file_contents=[ImageContent(logo_b64)],
            )
            _text, images = await chat.send_message_multimodal_response(msg)
            if not images:
                print(f"  [SKIP] No image returned for {rel_path}")
                return False

            png_bytes = base64.b64decode(images[0]["data"])
            png_bytes_to_webp(png_bytes, out_src)
            # copy to public as well
            png_bytes_to_webp(png_bytes, out_pub)
            print(f"  [OK]   {rel_path}  ({out_src.stat().st_size//1024}KB)")
            return True
        except Exception as e:
            print(f"  [FAIL] {rel_path} :: {e}")
            return False


async def main():
    with open(LOGO_PATH, "rb") as f:
        logo_b64 = base64.b64encode(f.read()).decode("utf-8")

    with open(CATALOG_PATH) as f:
        catalog = json.load(f)

    # Optional CLI args:
    #   --start N --end M   : slice of catalog to run (product-level batching)
    #   short-name ...      : whitelist specific products
    args = sys.argv[1:]
    start = 0
    end = len(catalog)
    only = set()
    i = 0
    while i < len(args):
        if args[i] == "--start":
            start = int(args[i + 1]); i += 2
        elif args[i] == "--end":
            end = int(args[i + 1]); i += 2
        else:
            only.add(args[i]); i += 1

    batch = catalog[start:end]

    tasks = []
    sem = asyncio.Semaphore(4)  # 4 concurrent image generations

    for product in batch:
        if only and product["short"] not in only:
            continue
        for rel in product["image"]:
            tasks.append(
                generate_one(logo_b64, product["short"], product["name"], rel, sem)
            )

    print(f"Generating {len(tasks)} images (products {start}..{end})...")
    results = await asyncio.gather(*tasks)
    ok = sum(1 for r in results if r)
    print(f"\nDone: {ok}/{len(tasks)} succeeded.")


if __name__ == "__main__":
    asyncio.run(main())
