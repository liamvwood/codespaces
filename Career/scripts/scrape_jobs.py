#!/usr/bin/env python3
"""
scrape_jobs.py — Playwright + BeautifulSoup job scraper for Liam Wood's job search.

Usage:
    python Career/scripts/scrape_jobs.py

Output:
    Career/jobs/applications_2026.csv  (appends new roles, skips duplicates)

Sources:
    - Direct company career pages (TARGETS list)
    - Jane Street JSON API  (janestreet.com/jobs/main.json)
    - Anthropic Greenhouse API
    - BuiltInAustin search (builtinaustin.com, 3 pages)

Requirements:
    pip install playwright beautifulsoup4 lxml
    python -m playwright install chromium
    # If Chromium fails to launch:
    sudo apt-get install -y libatk1.0-0 libatk-bridge2.0-0 libcups2 libdrm2 \
        libxkbcommon0 libxcomposite1 libxdamage1 libxfixes3 libxrandr2 libgbm1 libasound2t64
"""

import asyncio, csv, json, os, urllib.request
from pathlib import Path
from playwright.async_api import async_playwright
from bs4 import BeautifulSoup
from urllib.parse import urljoin

# ── Company → Track classification ────────────────────────────────────────────
BIGTECH_KEYWORDS = {"google","meta","apple","amazon","aws","microsoft","stripe",
                    "cloudflare","netflix","linkedin","salesforce","adobe","oracle"}
FINANCE_KEYWORDS = {"citadel","jane street","two sigma","jump trading","hrt",
                    "hudson river","blackrock","bloomberg","goldman","jpmorgan",
                    "morgan stanley","virtu","optiver","akuna","imc","de shaw",
                    "renaissance","point72"}

def classify(company: str) -> str:
    c = company.lower()
    if any(k in c for k in BIGTECH_KEYWORDS): return "BigTech"
    if any(k in c for k in FINANCE_KEYWORDS): return "Finance"
    return "Startup"

# ── Target career pages (generic Playwright scraper) ──────────────────────────
# Add or remove entries as needed: (Company, Track, URL)
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

# ── Keywords to match against job title text ──────────────────────────────────
KEYWORDS = [
    "infrastructure", "platform", "systems engineer", "reliability",
    "sre", "site reliability", "kubernetes", "devops", "distributed",
    "backend infrastructure", "production engineer", "compute", "accelerator",
    "sandboxing", "data infra", "ml infra", "agent infra",
]

RESUME_MAP = {
    "BigTech":  "Resume_BigTech_2026",
    "Finance":  "Resume_Finance_2026",
    "Startup":  "Resume_Startup_2026",
}

OUT_CSV = Path(__file__).parent.parent / "applications" / "applications_2026.csv"
FIELDS = ["Company", "Track", "Role", "URL", "Status", "Resume Variant", "Cover Letter", "Notes"]


async def scrape_page(page, company: str, track: str, url: str) -> list[dict]:
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
        results.append({
            "Company": company,
            "Track": track,
            "Role": title,
            "URL": href or "",
            "Status": "To Apply",
            "Resume Variant": RESUME_MAP.get(track, ""),
            "Cover Letter": "",
            "Notes": "",
        })

    # Strategy 1: anchor tags whose text looks like a job title
    for a in soup.find_all("a", href=True):
        add(a.get_text(strip=True), a["href"])

    # Strategy 2: headings near a link
    for tag in soup.find_all(["h2", "h3", "h4"]):
        text = tag.get_text(strip=True)
        nearby_a = tag.find_parent("a") or tag.find("a") or tag.find_next_sibling("a")
        href = nearby_a["href"] if nearby_a and nearby_a.get("href") else ""
        add(text, href)

    return results


def _make_row(company: str, role: str, url: str, track: str = None) -> dict:
    track = track or classify(company)
    return {"Company": company, "Track": track, "Role": role, "URL": url,
            "Status": "To Apply", "Resume Variant": RESUME_MAP.get(track, ""),
            "Cover Letter": "", "Notes": ""}


def scrape_jane_street() -> list[dict]:
    """Fetch Jane Street roles from their public JSON API."""
    rows = []
    try:
        with urllib.request.urlopen("https://www.janestreet.com/jobs/main.json", timeout=10) as r:
            jobs = json.loads(r.read())
        for j in jobs:
            title = j.get("position", "")
            if any(kw in title.lower() for kw in KEYWORDS):
                url = f"https://www.janestreet.com/join-jane-street/open-roles/?id={j['id']}"
                rows.append(_make_row("Jane Street", title, url, "Finance"))
    except Exception as e:
        print(f"  [Jane Street API] error: {e}")
    return rows


def scrape_greenhouse(company: str, board_slug: str, track: str) -> list[dict]:
    """Fetch roles from any Greenhouse job board API."""
    rows = []
    try:
        url = f"https://boards-api.greenhouse.io/v1/boards/{board_slug}/jobs?content=true"
        with urllib.request.urlopen(url, timeout=10) as r:
            data = json.loads(r.read())
        for j in data.get("jobs", []):
            title = j.get("title", "")
            if any(kw in title.lower() for kw in KEYWORDS):
                rows.append(_make_row(company, title, j.get("absolute_url", ""), track))
    except Exception as e:
        print(f"  [{company} Greenhouse] error: {e}")
    return rows


async def scrape_builtinaustin(browser, ua: str) -> list[dict]:
    """Scrape BuiltInAustin DevOps/infra search across all pages."""
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
                    rows.append(_make_row(company, title, href))
        except Exception as e:
            print(f"  [BuiltInAustin pg{pg}] error: {e}")
        finally:
            await page.close()
    return rows


async def main():
    # Load existing roles to avoid duplicates
    existing = set()
    if OUT_CSV.exists():
        with open(OUT_CSV, newline="") as f:
            for row in csv.DictReader(f):
                existing.add((row["Company"].strip(), row["Role"].strip()))

    all_new = []
    ua = "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"

    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)

        # Generic career page scraper
        page = await browser.new_page(user_agent=ua)
        for company, track, url in TARGETS:
            print(f"Scraping {company} ({track})...")
            jobs = await scrape_page(page, company, track, url)
            new_jobs = [j for j in jobs if (j["Company"], j["Role"]) not in existing]
            print(f"  → {len(jobs)} matched, {len(new_jobs)} new")
            all_new.extend(new_jobs)
            existing.update((j["Company"], j["Role"]) for j in new_jobs)
        await page.close()

        # BuiltInAustin (paginated, card-based)
        print("Scraping BuiltInAustin...")
        bia_jobs = await scrape_builtinaustin(browser, ua)
        new_bia = [j for j in bia_jobs if (j["Company"], j["Role"]) not in existing]
        print(f"  → {len(bia_jobs)} total, {len(new_bia)} new")
        all_new.extend(new_bia)
        existing.update((j["Company"], j["Role"]) for j in new_bia)

        await browser.close()

    # JSON API sources (no browser needed)
    print("Scraping Jane Street (API)...")
    js_jobs = scrape_jane_street()
    new_js = [j for j in js_jobs if (j["Company"], j["Role"]) not in existing]
    print(f"  → {len(js_jobs)} matched, {len(new_js)} new")
    all_new.extend(new_js)
    existing.update((j["Company"], j["Role"]) for j in new_js)

    print("Scraping Anthropic (Greenhouse API)...")
    anth_jobs = scrape_greenhouse("Anthropic", "anthropic", "Startup")
    new_anth = [j for j in anth_jobs if (j["Company"], j["Role"]) not in existing]
    print(f"  → {len(anth_jobs)} matched, {len(new_anth)} new")
    all_new.extend(new_anth)
    existing.update((j["Company"], j["Role"]) for j in new_anth)

    print("Scraping Anduril (Greenhouse API)...")
    and_jobs = scrape_greenhouse("Anduril", "andurilindustries", "Startup")
    new_and = [j for j in and_jobs if (j["Company"], j["Role"]) not in existing]
    print(f"  → {len(and_jobs)} matched, {len(new_and)} new")
    all_new.extend(new_and)

    # Write / append CSV
    write_header = not OUT_CSV.exists() or os.path.getsize(OUT_CSV) == 0
    OUT_CSV.parent.mkdir(parents=True, exist_ok=True)
    with open(OUT_CSV, "a", newline="") as f:
        w = csv.DictWriter(f, fieldnames=FIELDS)
        if write_header:
            w.writeheader()
        w.writerows(all_new)

    print(f"\nDone — wrote {len(all_new)} new roles to {OUT_CSV}")


if __name__ == "__main__":
    asyncio.run(main())
