#!/usr/bin/env python3
"""
scrape_jobs.py — Playwright + BeautifulSoup job scraper for Liam Wood's job search.

Usage:
    python Career/scripts/scrape_jobs.py

Output:
    Career/jobs/applications_2026.csv  (appends new roles, skips duplicates)

Requirements:
    pip install playwright beautifulsoup4 lxml
    python -m playwright install chromium
    python -m playwright install-deps chromium  # or: sudo apt-get install libatk1.0-0 ...
"""

import asyncio, csv, os
from pathlib import Path
from playwright.async_api import async_playwright
from bs4 import BeautifulSoup
from urllib.parse import urljoin

# ── Target career pages ────────────────────────────────────────────────────────
# Add or remove entries as needed: (Company, Track, URL)
TARGETS = [
    # Big Tech
    ("Google",      "BigTech",  "https://www.google.com/about/careers/applications/jobs/results?q=infrastructure+engineer&employment_type=FULL_TIME"),
    ("Meta",        "BigTech",  "https://www.metacareers.com/jobs?q=infrastructure+engineer&teams[0]=Infrastructure"),
    ("Stripe",      "BigTech",  "https://stripe.com/jobs/search#query=infrastructure"),
    ("Cloudflare",  "BigTech",  "https://www.cloudflare.com/careers/jobs/?department=Engineering"),
    ("AWS",         "BigTech",  "https://www.amazon.jobs/en/search?base_query=infrastructure+engineer&job_type=Full-Time"),
    # Finance / HFT
    ("Jane Street", "Finance",  "https://www.janestreet.com/join-jane-street/open-roles/"),
    ("Two Sigma",   "Finance",  "https://careers.twosigma.com/careers/SearchJobs/?485_484_484_parent_Department_TargetID=17866&listFilterMode=1"),
    ("Citadel",     "Finance",  "https://www.citadel.com/careers/open-opportunities/students/engineering/"),
    ("Jump Trading","Finance",  "https://www.jumptrading.com/careers/?"),
    # Startups
    ("Databricks",  "Startup",  "https://www.databricks.com/company/careers/open-positions?department=Engineering%20-%20Infrastructure"),
    ("Anduril",     "Startup",  "https://job-boards.greenhouse.io/andurilindustries"),
    ("Rippling",    "Startup",  "https://www.rippling.com/careers#open-positions"),
    ("Figma",       "Startup",  "https://www.figma.com/careers/#job-openings"),
]

# Keywords to match against job title text
KEYWORDS = [
    "infrastructure", "platform", "systems engineer", "reliability",
    "sre", "site reliability", "kubernetes", "devops", "distributed",
    "backend infrastructure", "production engineer",
]

RESUME_MAP = {
    "BigTech":  "Resume_BigTech_2026",
    "Finance":  "Resume_Finance_2026",
    "Startup":  "Resume_Startup_2026",
}

OUT_CSV = Path(__file__).parent.parent / "jobs" / "applications_2026.csv"
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


async def main():
    # Load existing roles to avoid duplicates
    existing = set()
    if OUT_CSV.exists():
        with open(OUT_CSV, newline="") as f:
            for row in csv.DictReader(f):
                existing.add((row["Company"], row["Role"]))

    all_new = []
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page(user_agent=(
            "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 "
            "(KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
        ))
        for company, track, url in TARGETS:
            print(f"Scraping {company} ({track})...")
            jobs = await scrape_page(page, company, track, url)
            new_jobs = [j for j in jobs if (j["Company"], j["Role"]) not in existing]
            print(f"  → {len(jobs)} matched, {len(new_jobs)} new")
            all_new.extend(new_jobs)
        await browser.close()

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
