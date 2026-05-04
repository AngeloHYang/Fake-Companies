#!/usr/bin/env python3
"""
Translate Harrison Financial and SecureStar websites into 6 languages.

Creates one subdirectory per language under each site root:
  harrison-financial/{zh-hans,zh-hant,es,fr,ja,ko}/*.html
  securestar/{zh-hans,zh-hant,es,fr,ja,ko}/*.html

Also adds a 🌐 language-switcher dropdown to every page.

Usage:
    python translate_websites.py
"""

import re
import time
from pathlib import Path

try:
    from openai import OpenAI
except ImportError:
    raise SystemExit("openai package not installed.  Run: pip install openai")


# ── Configuration ────────────────────────────────────────────────────────────

API_KEY = ""

# (dir-code, English name for translation prompt, HTML lang attr, native label)
LANGUAGES = [
    ("zh-hans", "Simplified Chinese",  "zh-Hans", "简体中文"),
    ("zh-hant", "Traditional Chinese", "zh-Hant", "繁體中文"),
    ("es",      "Spanish",             "es",       "Español"),
    ("fr",      "French",              "fr",       "Français"),
    ("ja",      "Japanese",            "ja",       "日本語"),
    ("ko",      "Korean",              "ko",       "한국어"),
]

SITES = {
    "harrison-financial": [
        "index.html", "about.html", "banking.html",
        "cards.html", "lending.html", "security.html",
        "support.html", "careers.html",
    ],
    "securestar": [
        "index.html", "company.html", "platform.html",
        "solutions.html", "developers.html",
    ],
}

# Try gpt-4o first; fall back to gpt-4o-mini if quota/rate error
CHAT_MODELS = ("gpt-4o", "gpt-4o-mini")

# ── Language-switcher widget ─────────────────────────────────────────────────

_SWITCHER_STYLE = (
    'style="display:flex;align-items:center;gap:6px;margin-left:12px;"'
)
_SELECT_STYLE = (
    'style="border:1.5px solid rgba(128,128,128,0.3);border-radius:6px;'
    'padding:4px 8px;font-size:0.82rem;background:transparent;'
    'color:inherit;cursor:pointer;outline:none;"'
)


def _build_options(page_name: str, current_code: str, is_original: bool) -> str:
    lines = []
    # English option
    if is_original:
        lines.append('<option value="" selected>English</option>')
    else:
        lines.append(f'<option value="../{page_name}">English</option>')
    # Other languages
    for code, _, _, native in LANGUAGES:
        if is_original:
            href = f'{code}/{page_name}'
        else:
            href = f'../{code}/{page_name}'
        sel = ' selected' if code == current_code else ''
        lines.append(f'<option value="{href}"{sel}>{native}</option>')
    return '\n            '.join(lines)


def make_switcher(page_name: str, current_code: str, is_original: bool) -> str:
    onchange = (
        "if(this.value)window.location.href=this.value"
        if is_original
        else "window.location.href=this.value"
    )
    opts = _build_options(page_name, current_code, is_original)
    return (
        f'<div class="lang-switcher" {_SWITCHER_STYLE}>\n'
        f'      <span style="font-size:1rem;line-height:1;">🌐</span>\n'
        f'      <select onchange="{onchange}" {_SELECT_STYLE}>\n'
        f'            {opts}\n'
        f'      </select>\n'
        f'    </div>'
    )


def inject_into_nav(html: str, widget: str) -> str:
    """Insert widget just before the last </div> inside <nav>…</nav>."""
    nav_re = re.compile(r'(<nav\b[^>]*>)(.*?)(</nav>)', re.DOTALL | re.IGNORECASE)
    m = nav_re.search(html)
    if not m:
        return html  # no <nav> found — leave unchanged
    nav_open, nav_body, nav_close = m.group(1), m.group(2), m.group(3)
    last = nav_body.rfind('</div>')
    if last == -1:
        return html
    new_body = nav_body[:last] + '\n    ' + widget + '\n  ' + nav_body[last:]
    return html[:m.start()] + nav_open + new_body + nav_close + html[m.end():]


def strip_switcher(html: str) -> str:
    """Remove any existing lang-switcher div (prevents duplication)."""
    return re.sub(
        r'\n?\s*<div class="lang-switcher"[^>]*>.*?</div>',
        '',
        html,
        flags=re.DOTALL,
    )

# ── Asset-path fixing ────────────────────────────────────────────────────────

def fix_asset_paths(html: str) -> str:
    """Rewrite images/* → ../images/* for pages one level below the site root."""
    return re.sub(r'((?:src|href)=["\'])images/', r'\1../images/', html)

# ── HTML lang attr ───────────────────────────────────────────────────────────

def set_lang_attr(html: str, lang_code: str) -> str:
    return re.sub(
        r'(<html\b[^>]*?\blang=)["\'][^"\']*["\']',
        r'\g<1>"' + lang_code + '"',
        html, count=1, flags=re.IGNORECASE,
    )

# ── CSS extraction (reduces token count ≈ 50%) ──────────────────────────────

def extract_styles(html: str):
    """Replace <style> blocks with placeholders; return (stripped_html, styles)."""
    styles = []

    def _repl(m):
        styles.append(m.group(0))
        return f'<!--STYLE_{len(styles) - 1}-->'

    stripped = re.sub(
        r'<style\b[^>]*>.*?</style>', _repl, html,
        flags=re.DOTALL | re.IGNORECASE,
    )
    return stripped, styles


def reinsert_styles(html: str, styles: list) -> str:
    for i, block in enumerate(styles):
        html = html.replace(f'<!--STYLE_{i}-->', block)
    return html

# ── OpenAI translation ───────────────────────────────────────────────────────

_SYSTEM = """\
You are a professional website translator specialising in fintech and banking.
Translate ALL visible user-facing text in the HTML document into {lang_name} ({lang_native}).

Strict rules:
• Return ONLY the complete translated HTML — no markdown fences, no commentary.
• Translate text between HTML tags; also translate alt, placeholder, and title attribute values.
• DO NOT translate: CSS code, JavaScript code, class names, IDs, href values, src values, HTML attribute names.
• DO NOT translate brand names: Harrison Financial, SecureStar, VISA, FDIC, Mastercard.
• DO NOT translate acronyms: APY, AML, KYC, ACH, MFA, API, SDK, SOC 2, ISO 27001, PCI DSS, GDPR, REST, JSON.
• Keep ALL numbers, percentages, and currency amounts exactly as-is (e.g. $0, 4.85%, $250,000, 3M+).
• Keep ALL URLs unchanged.
• Keep 'HF' and 'SS' in logo-icon divs unchanged.
• Keep <!--STYLE_N--> placeholder comments exactly as-is (they will be replaced later).
• Preserve all HTML structure, indentation, and tag attributes verbatim.
• Use professional, natural language appropriate for a fintech/banking audience in the target locale.
"""


def translate_html(client: OpenAI, html: str, lang_name: str, lang_native: str) -> str:
    system = _SYSTEM.format(lang_name=lang_name, lang_native=lang_native)
    last_exc = None
    for model in CHAT_MODELS:
        try:
            resp = client.chat.completions.create(
                model=model,
                messages=[
                    {"role": "system", "content": system},
                    {"role": "user",   "content": html},
                ],
                temperature=0.15,
                max_tokens=16000,
            )
            raw = resp.choices[0].message.content.strip()
            # Strip accidental markdown code fences
            raw = re.sub(r'^```[a-z]*\n?', '', raw)
            raw = re.sub(r'\n?```$', '',   raw)
            return raw.strip()
        except Exception as exc:
            last_exc = exc
            print(f"\n      ! {model} error: {exc}", end='')
    raise RuntimeError(str(last_exc))

# ── Per-site processing ──────────────────────────────────────────────────────

def process_site(client: OpenAI, site: str, pages: list) -> None:
    site_dir = Path(site)
    print(f"\n{'='*62}")
    print(f"  Site: {site}")
    print(f"{'='*62}")

    # Step 1 — inject language switcher into original English pages
    print("\n  [en] Adding language switcher to originals…")
    for page in pages:
        path = site_dir / page
        if not path.exists():
            print(f"    SKIP (missing): {page}")
            continue
        html = path.read_text(encoding='utf-8')
        if 'lang-switcher' in html:
            print(f"    already done:  {page}")
            continue
        widget = make_switcher(page, 'en', is_original=True)
        html   = inject_into_nav(html, widget)
        path.write_text(html, encoding='utf-8')
        print(f"    ✓ {page}")

    # Step 2 — translate each page into each target language
    for code, eng_name, html_lang, native in LANGUAGES:
        lang_dir = site_dir / code
        lang_dir.mkdir(exist_ok=True)
        print(f"\n  [{eng_name} / {code}]")

        for page in pages:
            src = site_dir / page
            dst = lang_dir / page
            if not src.exists():
                continue

            print(f"    {page}…", end=' ', flush=True)

            html = src.read_text(encoding='utf-8')
            # Remove switcher so it isn't sent to the AI or duplicated
            html = strip_switcher(html)
            # Fix relative asset paths for a page one dir deeper
            html = fix_asset_paths(html)
            # Extract <style> blocks to slash token count in half
            html_stripped, styles = extract_styles(html)

            try:
                translated = translate_html(client, html_stripped, eng_name, native)
                # Restore style blocks
                translated = reinsert_styles(translated, styles)
                # Set correct HTML lang attribute
                translated = set_lang_attr(translated, html_lang)
                # Inject language switcher (post-translation)
                widget = make_switcher(page, code, is_original=False)
                if 'lang-switcher' not in translated:
                    translated = inject_into_nav(translated, widget)

                dst.write_text(translated, encoding='utf-8')
                complete = re.search(r'</html\s*>', translated, re.IGNORECASE)
                print("✓" if complete else "⚠ (possibly truncated)")
            except Exception as exc:
                print(f"✗  {exc}")

            time.sleep(1)   # gentle rate-limit buffer


# ── Entry point ──────────────────────────────────────────────────────────────

def main() -> None:
    client  = OpenAI(api_key=API_KEY)
    n_pages = sum(len(v) for v in SITES.values())
    n_langs = len(LANGUAGES)
    print(
        f"Translating {n_pages} pages × {n_langs} languages = {n_pages * n_langs} files\n"
        f"Chat models: {' → '.join(CHAT_MODELS)}\n"
    )
    for site, pages in SITES.items():
        process_site(client, site, pages)
    print("\n✓ Translation complete!")


if __name__ == "__main__":
    main()
