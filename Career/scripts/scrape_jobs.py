#!/usr/bin/env python3
"""
scrape_jobs.py — Playwright + BeautifulSoup job scraper for Liam Wood's job search.

Usage:
    python Career/scripts/scrape_jobs.py

Output:
    Career/applications/applications_2026.csv  (appends new roles, skips duplicates)

Sources:
    - Direct company career pages (TARGETS list)         — generic Playwright scraper
    - Jane Street JSON API  (janestreet.com/jobs/main.json)
    - Greenhouse API         — Anthropic, Anduril, Virtu
    - BuiltInAustin search   — builtinaustin.com, 3 pages
    - HRT (Hudson River Trading) — WP admin-ajax.php (action=get_hrt_jobs_handler)
    - Ongig API              — Apex Fintech Solutions / Peak6

Location filter: New York, Austin, Miami, Remote (TARGET_LOCS)

Requirements:
    pip install playwright beautifulsoup4 lxml
    python -m playwright install chromium
    # If Chromium fails to launch:
    sudo apt-get install -y libatk1.0-0 libatk-bridge2.0-0 libcups2 libdrm2 \\
        libxkbcommon0 libxcomposite1 libxdamage1 libxfixes3 libxrandr2 libgbm1 libasound2t64
"""

import asyncio, csv, json, os, urllib.request, urllib.parse
from pathlib import Path
from playwright.async_api import async_playwright
from bs4 import BeautifulSoup
from urllib.parse import urljoin

# ── Location filter ────────────────────────────────────────────────────────────
TARGET_LOCS = ["new york", "austin", "miami", "nyc", "remote"]

def in_target_location(loc) -> bool:
    if not loc:
        return False
    return any(t in loc.lower() for t in TARGET_LOCS)

# ── Company → Track classification ────────────────────────────────────────────
BIGTECH_KEYWORDS = {"google","meta","apple","amazon","aws","microsoft","stripe",
                    "cloudflare","netflix","linkedin","salesforce","adobe","oracle"}
FINANCE_KEYWORDS = {"citadel","jane street","two sigma","jump trading","hrt",
                    "hudson river","blackrock","bloomberg","goldman","jpmorgan",
                    "morgan stanley","virtu","optiver","akuna","imc","de shaw",
                    "renaissance","point72","peak6","apex fintech"}

def classify(company: str) -> str:
    c = company.lower()
    if any(k in c for k in BIGTECH_KEYWORDS): return "BigTech"
    if any(k in c for k in FINANCE_KEYWORDS): return "Finance"
    return "Startup"

# ── Target career pages (generic Playwright scraper) ──────────────────────────
TARGETS = [
    # Big Tech
    ("Google",      "BigTech",  "https://www.google.com/about/careers/applications/jobs/results?q=infrastructure+engineer&employment_type=FULL_TIME"),
    ("Meta",        "BigTech",  "https://www.metacareers.com/jobs?q=infrastructure+engineer&teams[0]=Infrastructure"),
    ("Stripe",      "BigTech",  "https://stripe.com/jobs/search#query=infrastructure"),
    ("Cloudflare",  "BigTech",  "https://www.cloudflare.com/careers/jobs/?department=Engineering"),
    ("AWS",         "BigTech",  "https://www.amazon.jobs/en/search?base_query=infrastructure+engineer&job_type=Full-Time"),
    # Finance / HFT
    ("Citadel",     "Finance",  "https://www.citadel.com/careers/open-opportunities/students/engineering/"),
    ("Jump Trading","Finance",  "https://www.jumptrading.com/careers/?"),
    # Startups
    ("Databricks",  "Startup",  "https://www.databricks.com/company/careers/open-positions?department=Engineering%20-%20Infrastructure"),
    ("Rippling",    "Startup",  "https://www.rippling.com/careers#open-positions"),
    ("Figma",       "Startup",  "https://www.figma.com/careers/#job-openings"),
]

# ── Keywords to match against job title ───────────────────────────────────────
KEYWORDS = [
    "infrastructure", "platform", "systems engineer", "reliability",
    "sre", "site reliability", "kubernetes", "devops", "distributed",
    "backend infrastructure", "production engineer", "compute", "accelerator",
    "sandboxing", "data infra", "ml infra", "agent infra", "network engineer",
    "storage engineer", "gpu", "hpc", "software engineer", "backend engineer",
]

RESUME_MAP = {
    "BigTech":  "Resume_BigTech_2026",
    "Finance":  "Resume_Finance_2026",
    "Startup":  "Resume_Startup_2026",
}

OUT_CSV = Path(__file__).parent.parent / "applications" / "applications_2026.csv"
FIELDS = ["Company", "Track", "Role", "URL", "Status", "Resume Variant", "Cover Letter", "Notes", "Location"]


def _make_row(company: str, role: str, url: str, track: str = None, location: str = "") -> dict:
    track = track or classify(company)
    return {"Company": company, "Track": track, "Role": role, "URL": url,
            "Status": "To Apply", "Resume Variant": RESUME_MAP.get(track, ""),
            "Cover Letter": "", "Notes": "", "Location": location}


async def scrape_page(page, company: str, track: str, url: str) -> list[dict]:
    """Generic career page scraper — keyword-filtered anchor/heading extraction."""
    results = []
    try:
        await page.goto(url, timeout=25000, wait_until="domcontentloaded")
        await page.wait_for_timeout(3000)
        soup = BeautifulSoup(await page.content(), "lxml")
    except Exception as e:
        print(f"  [{company}] fetch error: {e}")
        return []

    seen_titles = set()

    def add(title: str, href: str):
        title = title.strip()
        if not title or len(title) < 8 or len(title) > 130:
            return
        if not any(kw in title.lower() for kw in KEYWORDS):
            return
        if title in seen_titles:
            return
        seen_titles.add(title)
        if href and not href.startswith("http"):
            href = urljoin(url, href)
        results.append(_make_row(company, title, href or "", track))

    for a in soup.find_all("a", href=True):
        add(a.get_text(strip=True), a["href"])
    for tag in soup.find_all(["h2", "h3", "h4"]):
        text = tag.get_text(strip=True)
        nearby_a = tag.find_parent("a") or tag.find("a") or tag.find_next_sibling("a")
        href = nearby_a["href"] if nearby_a and nearby_a.get("href") else ""
        add(text, href)

    return results


def scrape_jane_street() -> list[dict]:
    """Jane Street public JSON API — filters to NYC only."""
    rows = []
    try:
        with urllib.request.urlopen("https://www.janestreet.com/jobs/main.json", timeout=10) as r:
            jobs = json.loads(r.read())
        for j in jobs:
            title = j.get("position", "")
            city = j.get("city", "")
            if any(kw in title.lower() for kw in KEYWORDS) and in_target_location(city):
                url = f"https://www.janestreet.com/join-jane-street/open-roles/?id={j['id']}"
                rows.append(_make_row("Jane Street", title, url, "Finance", city))
    except Exception as e:
        print(f"  [Jane Street API] error: {e}")
    return rows


def scrape_greenhouse(company: str, board_slug: str, track: str) -> list[dict]:
    """Greenhouse job board API — filters to target locations."""
    rows = []
    try:
        url = f"https://boards-api.greenhouse.io/v1/boards/{board_slug}/jobs?content=true"
        with urllib.request.urlopen(url, timeout=10) as r:
            data = json.loads(r.read())
        for j in data.get("jobs", []):
            title = j.get("title", "")
            loc = j.get("location", {}).get("name", "")
            if any(kw in title.lower() for kw in KEYWORDS) and in_target_location(loc):
                rows.append(_make_row(company, title, j.get("absolute_url", ""), track, loc))
    except Exception as e:
        print(f"  [{company} Greenhouse] error: {e}")
    return rows


async def scrape_builtinaustin(browser, ua: str) -> list[dict]:
    """BuiltInAustin DevOps/infra search — already Austin-focused."""
    rows = []
    seen = set()
    base = "https://www.builtinaustin.com/jobs?search=Senior+DevOps+Engineer"
    for pg in range(1, 4):
        url = f"{base}&page={pg}" if pg > 1 else base
        page = await browser.new_page(user_agent=ua)
        try:
            await page.goto(url, timeout=30000, wait_until="networkidle")
            await page.wait_for_timeout(3000)
            soup = BeautifulSoup(await page.content(), "lxml")
            cards = soup.find_all("div", attrs={"data-id": "job-card"})
            print(f"  BuiltInAustin page {pg}: {len(cards)} cards")
            for card in cards:
                co_tag = card.find("a", attrs={"data-id": "company-title"}) or \
                         card.find("a", href=lambda h: h and h.startswith("/company/"))
                company = co_tag.get_text(strip=True) if co_tag else "Unknown"
                title_tag = card.find("a", attrs={"data-id": "job-card-title"}) or card.find("h2")
                if not title_tag: continue
                title = title_tag.get_text(strip=True)
                href  = title_tag.get("href", "")
                if href and not href.startswith("http"):
                    href = "https://www.builtinaustin.com" + href
                key = (company, title)
                if key not in seen:
                    seen.add(key)
                    rows.append(_make_row(company, title, href, location="Austin, TX"))
        except Exception as e:
            print(f"  [BuiltInAustin pg{pg}] error: {e}")
        finally:
            await page.close()
    return rows


async def scrape_hrt(browser, ua: str) -> list[dict]:
    """Hudson River Trading — WP admin-ajax.php with get_hrt_jobs_handler action.
    Requires a fresh nonce from the careers page.
    Filters to NYC, Austin, Miami.
    """
    rows = []
    page = await browser.new_page(user_agent=ua)
    try:
        await page.goto("https://www.hudsonrivertrading.com/careers/", timeout=30000, wait_until="networkidle")
        nonce_json = await page.evaluate("() => JSON.stringify(window.hrtJobsAjax || {})")
        nonce_data = json.loads(nonce_json)
        nonce = nonce_data.get("nonce", "")
        ajax_url = nonce_data.get("ajaxurl", "https://www.hudsonrivertrading.com/wp-admin/admin-ajax.php")
        cookies = await page.context.cookies()
        cookie_str = "; ".join(f"{c['name']}={c['value']}" for c in cookies)
    finally:
        await page.close()

    if not nonce:
        print("  [HRT] could not retrieve nonce")
        return rows

    setting = json.dumps({
        "meta_data": [{"icon":"","term":"locations"},{"icon":"","term":"job-category"},{"icon":"","term":"job-type"}],
        "settings": {"hide_job_id": True}
    })
    post_data = urllib.parse.urlencode({
        "action": "get_hrt_jobs_handler",
        "data[search]": "",
        "setting": setting,
        "_ajax_nonce": nonce,
    }).encode()

    req = urllib.request.Request(ajax_url, data=post_data, headers={
        "User-Agent": ua,
        "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
        "X-Requested-With": "XMLHttpRequest",
        "Referer": "https://www.hudsonrivertrading.com/careers/",
        "Cookie": cookie_str,
    })
    try:
        with urllib.request.urlopen(req, timeout=15) as r:
            jobs = json.loads(r.read())
    except Exception as e:
        print(f"  [HRT ajax] error: {e}")
        return rows

    import html
    for j in jobs:
        title = html.unescape(j.get("title", ""))
        soup = BeautifulSoup(j.get("content", ""), "lxml")
        card = soup.find(class_="hrt-card-item")
        term = card["data-term"] if card and card.has_attr("data-term") else ""

        # Parse first matching target location from term
        loc_raw = ""
        for part in term.split("==="):
            if any(t.replace(" ", "-") in part for t in ["new-york", "austin", "miami"]):
                loc_raw = part.replace("-", " ").title()
                break
        in_target = bool(loc_raw)

        link = soup.find("a", href=True)
        url = link["href"] if link else "https://www.hudsonrivertrading.com/careers/"

        if any(kw in title.lower() for kw in KEYWORDS) and in_target:
            rows.append(_make_row("Hudson River Trading", title, url, "Finance", loc_raw))

    return rows


def scrape_ongig(company: str, api_token: str, track: str, base_url: str) -> list[dict]:
    """Ongig job search API — paginates all results, filters by title keyword + location.
    bearer token is embedded in the Ongig embed script hosted on CloudFront.
    """
    rows = []
    page_num = 1
    while True:
        payload = {
            "query": "",
            "result_fields": {
                "title": {"raw": {}}, "location": {"raw": {}},
                "url": {"raw": {}}, "city_filter": {"raw": {}},
                "country_filter": {"raw": {}}, "subdivision": {"raw": {}},
            },
            "page": {"size": 100, "current": page_num},
        }
        try:
            req = urllib.request.Request(
                "https://text-analyzer.ongig.com/api/external/v1/jobs/search",
                data=json.dumps(payload).encode(),
                headers={
                    "Authorization": f"Bearer {api_token}",
                    "Content-Type": "application/json",
                    "User-Agent": "Mozilla/5.0",
                    "Referer": base_url,
                }
            )
            with urllib.request.urlopen(req, timeout=15) as r:
                data = json.loads(r.read())
        except Exception as e:
            print(f"  [{company} Ongig p{page_num}] error: {e}")
            break

        jobs = data.get("results", [])
        meta = data.get("meta", {}).get("page", {})
        for j in jobs:
            title = j.get("title", {}).get("raw", "")
            loc = j.get("location", {}).get("raw", "")
            url_path = j.get("url", {}).get("raw", "")
            full_url = f"{base_url.rstrip('/')}/jobs/{url_path}"
            if any(kw in title.lower() for kw in KEYWORDS) and in_target_location(loc):
                rows.append(_make_row(company, title, full_url, track, loc))

        if page_num >= meta.get("total_pages", 1):
            break
        page_num += 1

    return rows


async def main():
    # Load existing roles to avoid duplicates; preserve Location column if present
    existing = set()
    existing_rows = []
    fieldnames = FIELDS
    if OUT_CSV.exists():
        with open(OUT_CSV, newline="") as f:
            reader = csv.DictReader(f)
            fieldnames = reader.fieldnames or FIELDS
            if "Location" not in fieldnames:
                fieldnames = list(fieldnames) + ["Location"]
            for row in reader:
                row.setdefault("Location", "")
                existing_rows.append(row)
                existing.add((row["Company"].strip(), row["Role"].strip()))

    all_new: list[dict] = []
    ua = "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"

    def add_new(jobs: list[dict]):
        for j in jobs:
            j.setdefault("Location", "")
            key = (j["Company"].strip(), j["Role"].strip())
            if key not in existing:
                existing.add(key)
                all_new.append(j)

    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)

        # Generic career page scraper (location not filtered — pages are already role-specific)
        page = await browser.new_page(user_agent=ua)
        for company, track, url in TARGETS:
            print(f"Scraping {company} ({track})...")
            jobs = await scrape_page(page, company, track, url)
            before = len(all_new)
            add_new(jobs)
            print(f"  → {len(jobs)} matched, {len(all_new)-before} new")
        await page.close()

        # BuiltInAustin (paginated, card-based, Austin-focused)
        print("Scraping BuiltInAustin...")
        add_new(await scrape_builtinaustin(browser, ua))

        # HRT (requires browser for nonce)
        print("Scraping HRT (admin-ajax)...")
        hrt_jobs = await scrape_hrt(browser, ua)
        before = len(all_new)
        add_new(hrt_jobs)
        print(f"  → {len(hrt_jobs)} matched, {len(all_new)-before} new")

        await browser.close()

    # API-only sources
    print("Scraping Jane Street (API)...")
    add_new(scrape_jane_street())

    for company, slug, track in [
        ("Anthropic",     "anthropic",        "Startup"),
        ("Anduril",       "andurilindustries", "Startup"),
        ("Virtu Financial","virtu",            "Finance"),
    ]:
        print(f"Scraping {company} (Greenhouse API)...")
        add_new(scrape_greenhouse(company, slug, track))

    # Ongig — Apex Fintech Solutions / Peak6
    # Token from: https://d171fmx844et9o.cloudfront.net/peak6/2.0/ongig-embed.umd.js
    print("Scraping Apex Fintech Solutions / Peak6 (Ongig API)...")
    apex_jobs = scrape_ongig(
        company="Apex Fintech Solutions",
        api_token="1bb83b1b-7481-11df-bbeb-b11bb1cb11b4",
        track="Finance",
        base_url="https://careers.peak6.com",
    )
    before = len(all_new)
    add_new(apex_jobs)
    print(f"  → {len(apex_jobs)} matched, {len(all_new)-before} new")

    # Write full CSV (preserving existing rows + new)
    OUT_CSV.parent.mkdir(parents=True, exist_ok=True)
    with open(OUT_CSV, "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=FIELDS, extrasaction="ignore")
        w.writeheader()
        w.writerows(existing_rows)
        w.writerows(all_new)

    print(f"\nDone — wrote {len(all_new)} new roles to {OUT_CSV} (total {len(existing_rows)+len(all_new)})")


if __name__ == "__main__":
    asyncio.run(main())
