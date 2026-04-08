#!/usr/bin/env python3
"""Apply indexing + scaling controls for existing programmatic SEO pages."""

from __future__ import annotations

import argparse
import json
import re
from collections import Counter, defaultdict
from dataclasses import dataclass
from datetime import date
from pathlib import Path
from typing import Iterable

ROOT = Path(__file__).resolve().parents[1]
PSEO_DIR = ROOT / "pseo"
DATA_DIR = ROOT / "programmatic-seo" / "data"

DOMAIN = "https://keycitydigital.com"
TOP_CITIES = {"dallas", "fort-worth", "abilene", "midland", "lubbock"}
TOP_INDUSTRIES = {"roofing", "hvac", "plumbing"}
TOP_SERVICES = {"website-design", "local-seo", "google-maps"}

CORE_URLS = [
    "/",
    "/services/index.html",
    "/industries.html",
    "/contact.html",
    "/about.html",
    "/portfolio-results.html",
    "/texas-markets.html",
]

PHASES = {
    "week1-2": {"tier2_fraction": 0.0},
    "week3-4": {"tier2_fraction": 0.30},
    "month2": {"tier2_fraction": 0.65},
    "month3-plus": {"tier2_fraction": 1.0},
}

WORD_RE = re.compile(r"[a-zA-Z]{3,}")


@dataclass
class Page:
    path: Path
    url: str
    service: str
    industry: str
    city: str
    tier: str = "tier3"
    unique_score: float = 0.0
    similarity_neighbors: list[str] | None = None


def load_data(name: str) -> list[dict]:
    return json.loads((DATA_DIR / name).read_text())


def parse_page(path: Path) -> Page | None:
    parts = path.relative_to(PSEO_DIR).parts
    if len(parts) != 4 or parts[-1] != "index.html":
        return None
    service, industry, city_tx, _ = parts
    if not city_tx.endswith("-tx"):
        return None
    return Page(path=path, url=f"/{service}/{industry}/{city_tx}/", service=service, industry=industry, city=city_tx[:-3])


def tier_for(page: Page) -> str:
    if page.city in TOP_CITIES and page.industry in TOP_INDUSTRIES and page.service in TOP_SERVICES:
        return "tier1"
    if page.city in TOP_CITIES or page.industry in TOP_INDUSTRIES or page.service in TOP_SERVICES:
        return "tier2"
    return "tier3"


def token_set(html: str) -> set[str]:
    tokens = {w.lower() for w in WORD_RE.findall(html)}
    stop = {"class", "href", "https", "http", "section", "container", "digital", "texas", "city", "industry", "service"}
    return {t for t in tokens if t not in stop}


def jaccard(a: set[str], b: set[str]) -> float:
    if not a or not b:
        return 0.0
    return len(a & b) / len(a | b)


def evaluate_uniqueness(pages: list[Page]) -> None:
    token_map: dict[str, set[str]] = {}
    for p in pages:
        token_map[p.url] = token_set(p.path.read_text())

    for p in pages:
        sims: list[tuple[str, float]] = []
        for other in pages:
            if other.url == p.url:
                continue
            score = jaccard(token_map[p.url], token_map[other.url])
            sims.append((other.url, score))
        sims.sort(key=lambda item: item[1], reverse=True)
        top_neighbors = sims[:3]
        max_sim = top_neighbors[0][1] if top_neighbors else 0.0
        p.unique_score = round(1.0 - max_sim, 3)
        p.similarity_neighbors = [f"{u}:{s:.3f}" for u, s in top_neighbors]


def enforce_cta(html: str) -> list[str]:
    issues = []
    if "WebsiteLeakDetector.com" not in html:
        issues.append("missing_website_leak_detector_cta")
    if "api.leadconnectorhq.com/widget/bookings/digital-marketing-consultation-apykl" not in html:
        issues.append("missing_booking_cta")
    return issues


def set_robots_meta(html: str, robots_value: str) -> str:
    meta_line = f'  <meta name="robots" content="{robots_value}" />'
    if '<meta name="robots"' in html:
        return re.sub(r'\s*<meta name="robots" content="[^"]*"\s*/>\n?', f"\n{meta_line}\n", html, count=1)
    return html.replace("</head>", f"{meta_line}\n</head>", 1)


def set_tier_marker(html: str, tier: str) -> str:
    marker = f"<!-- pseo-tier:{tier} -->"
    if "<!-- pseo-tier:" in html:
        return re.sub(r"<!-- pseo-tier:[^>]+-->", marker, html, count=1)
    return html.replace("<main>", f"{marker}\n<main>", 1)


def render_sitemap(urls: Iterable[str]) -> str:
    lines = ['<?xml version="1.0" encoding="UTF-8"?>', '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">']
    for url in sorted(urls):
        lines.append(f"  <url><loc>{DOMAIN}{url}</loc><changefreq>weekly</changefreq><priority>0.8</priority></url>")
    lines.append("</urlset>")
    return "\n".join(lines) + "\n"


def main() -> None:
    parser = argparse.ArgumentParser(description="Apply indexing controls to generated PSEO pages")
    parser.add_argument("--phase", choices=sorted(PHASES.keys()), default="week1-2", help="Rollout phase to determine Tier 2 indexing unlock")
    args = parser.parse_args()

    pages = [p for p in (parse_page(path) for path in PSEO_DIR.rglob("index.html")) if p]
    if not pages:
        raise SystemExit("No PSEO pages found under pseo/")

    evaluate_uniqueness(pages)

    tiers: dict[str, list[Page]] = defaultdict(list)
    audit_issues: dict[str, list[str]] = {}

    for page in pages:
        page.tier = tier_for(page)
        html = page.path.read_text()

        issues = enforce_cta(html)
        if page.unique_score < 0.015:
            issues.append("low_uniqueness_score")
        if issues:
            audit_issues[page.url] = issues
            if page.tier == "tier1":
                page.tier = "tier2"

        if page.tier == "tier1":
            robots = "index,follow,max-snippet:-1,max-image-preview:large,max-video-preview:-1"
        elif page.tier == "tier2":
            robots = "noindex,follow"
        else:
            robots = "noindex,nofollow"

        html = set_robots_meta(html, robots)
        html = set_tier_marker(html, page.tier)
        page.path.write_text(html)

        tiers[page.tier].append(page)

    tier2_sorted = sorted(tiers["tier2"], key=lambda p: (p.unique_score, p.url), reverse=True)
    tier2_unlock = int(len(tier2_sorted) * PHASES[args.phase]["tier2_fraction"])
    tier2_index_now = [p.url for p in tier2_sorted[:tier2_unlock]]

    tier1_urls = [p.url for p in tiers["tier1"]]
    index_now = sorted(tier1_urls + tier2_index_now)
    defer_index = sorted([p.url for p in tier2_sorted[tier2_unlock:]])
    hold_urls = sorted([p.url for p in tiers["tier3"]])

    (PSEO_DIR / "sitemap-core.xml").write_text(render_sitemap(CORE_URLS))
    (PSEO_DIR / "sitemap-tier1.xml").write_text(render_sitemap(tier1_urls))
    (PSEO_DIR / "sitemap-tier2.xml").write_text(render_sitemap(tier2_index_now))

    sitemap_index = "\n".join([
        '<?xml version="1.0" encoding="UTF-8"?>',
        '<sitemapindex xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">',
        f"  <sitemap><loc>{DOMAIN}/pseo/sitemap-core.xml</loc></sitemap>",
        f"  <sitemap><loc>{DOMAIN}/pseo/sitemap-tier1.xml</loc></sitemap>",
        f"  <sitemap><loc>{DOMAIN}/pseo/sitemap-tier2.xml</loc></sitemap>",
        "</sitemapindex>",
        "",
    ])
    (PSEO_DIR / "sitemap-programmatic.xml").write_text(sitemap_index)

    tier_manifest = {
        "generated_on": date.today().isoformat(),
        "rollout_phase": args.phase,
        "counts": {tier: len(items) for tier, items in tiers.items()},
        "tier1": sorted([p.url for p in tiers["tier1"]]),
        "tier2": sorted([p.url for p in tiers["tier2"]]),
        "tier3": hold_urls,
    }
    (PSEO_DIR / "tier-classification.json").write_text(json.dumps(tier_manifest, indent=2))

    combo_counter = Counter((p.service, p.industry, p.city) for p in pages if p.url in index_now)
    performance_plan = {
        "metrics": ["impressions", "clicks", "average_position", "conversions", "cta_click_rate"],
        "group_by": ["service", "industry", "city", "tier"],
        "winning_cluster_rule": "Promote clusters with 2+ weeks above median CTR and conversion rate.",
        "current_indexed_combos": len(combo_counter),
    }

    strategy = {
        "generated_on": date.today().isoformat(),
        "rollout_phase": args.phase,
        "index_now": index_now,
        "defer_index": defer_index,
        "hold_future": hold_urls,
        "indexing_timeline": {
            "week1-2": "Index tier1 only; submit sitemap-core + sitemap-tier1.",
            "week3-4": "Unlock top 30% of tier2 by uniqueness/performance; keep remaining tier2 on noindex.",
            "month2": "Unlock up to 65% tier2, begin selective tier3 promotion after content refresh.",
            "month3-plus": "Full tier2 indexing and controlled tier3 entry based on winning clusters.",
        },
        "internal_linking_rules": {
            "tier1": "Linked from homepage/services/industry hubs and cross-linked between top city pages.",
            "tier2": "Linked primarily from tier1 pages and local cluster pages; keep global nav exposure limited.",
            "tier3": "Not included in hub lists. Keep direct links minimal until promoted.",
        },
        "performance_monitoring": performance_plan,
        "audit_issues": audit_issues,
        "ai_search_optimization": {
            "requirements": [
                "Direct Q&A sections retained",
                "Structured headings and concise answers",
                "FAQ + Breadcrumb + Service schema present",
            ]
        },
    }
    (PSEO_DIR / "indexing-strategy.json").write_text(json.dumps(strategy, indent=2))

    rollout_md = f"""# Programmatic SEO Indexing & Scaling Roadmap

Generated on: {date.today().isoformat()}  
Current rollout phase: **{args.phase}**

## Tier model
- **Tier 1 (index now):** Top city + top service + top industry combinations.
- **Tier 2 (delayed indexing):** Pages matching at least one priority axis.
- **Tier 3 (hold/future):** Long-tail pages with limited demand or weak uniqueness.

## Sitemaps
- `pseo/sitemap-core.xml`: Main site authority pages.
- `pseo/sitemap-tier1.xml`: Tier 1 URLs only.
- `pseo/sitemap-tier2.xml`: Tier 2 URLs that are currently unlocked for indexing.
- `pseo/sitemap-programmatic.xml`: Sitemap index referencing the files above.

## Rollout schedule
1. **Week 1-2:** Publish/index Tier 1 only.
2. **Week 3-4:** Unlock top 30% of Tier 2 URLs.
3. **Month 2+:** Expand Tier 2 and promote select Tier 3 pages after differentiation improvements.

## Internal linking controls
- **Tier 1:** Heaviest internal links (homepage, services hub, peer links).
- **Tier 2:** Controlled links from Tier 1/local clusters.
- **Tier 3:** Minimal linking until promoted.

## Differentiation gate
- Pages with low uniqueness score are held back from Tier 1 promotion.
- Any page missing required CTAs is blocked from indexing promotion.

## Performance monitoring
Track in Search Console + analytics by service/industry/city cluster:
- impressions
- clicks
- average position
- conversions
- CTA click-through rate

Promote clusters that maintain above-median CTR + conversion for at least 2 weeks.
"""
    (PSEO_DIR / "indexing-rollout-plan.md").write_text(rollout_md)

    print(json.dumps({"phase": args.phase, "tier1": len(tiers['tier1']), "tier2": len(tiers['tier2']), "tier3": len(tiers['tier3']), "tier2_unlocked": tier2_unlock}, indent=2))


if __name__ == "__main__":
    main()
