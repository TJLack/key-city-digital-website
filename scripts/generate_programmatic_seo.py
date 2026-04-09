#!/usr/bin/env python3
import argparse, json, hashlib
from pathlib import Path
from datetime import date

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "programmatic-seo" / "data"
OUT = ROOT / "pseo"
BOOKING = "https://api.leadconnectorhq.com/widget/bookings/digital-marketing-consultation-apykl"
SCAN = "https://WebsiteLeakDetector.com"

INTRO_VARIANTS = [
    "In {city}, {industry} companies compete hard for fast homeowner decisions. {service} helps you become the obvious choice before the first callback.",
    "{city} homeowners compare options quickly. {service} gives {industry} teams a clearer offer, better local visibility, and stronger conversion pathways.",
    "If you operate an {industry} business in {city}, {service} is often the difference between random leads and a predictable booked-job pipeline."
]
LOCAL_VARIANTS = [
    "{city} sits in the {metro_area} market, where contractor competition is {contractor_density}. That makes conversion quality and local relevance non-negotiable.",
    "In {city}, you are not just competing on price—you are competing on trust, visibility, and response speed. {service} improves all three.",
    "Because {city} is a {population_tier} market, homeowners often compare multiple providers before calling. Strong digital positioning improves your win rate."
]
PROBLEM_VARIANTS = [
    "Many {industry} companies in {city} rely on referrals and inconsistent lead flow. That creates cashflow volatility and unpredictable booking cycles.",
    "Most local competitors still use generic websites and broad messaging. That attracts low-intent traffic and weak conversion rates.",
    "Without tight local positioning, even good contractors get buried in maps and search when demand spikes."
]


def slugify(v: str) -> str:
    return v.lower().replace("&", "and").replace(" ", "-")


def pick_variant(key: str, variants):
    idx = int(hashlib.md5(key.encode()).hexdigest(), 16) % len(variants)
    return variants[idx]


def load(name):
    return json.loads((DATA / name).read_text())


def build_page(service, industry, city, mode="service-industry-city"):
    city_slug = f"{city['slug']}-tx"
    service_slug = service["slug"]
    industry_slug = industry["slug"]

    if mode == "service-city":
        url = f"/{service_slug}/{city_slug}/"
        path = OUT / service_slug / city_slug / "index.html"
        h1 = f"{service['service']} in {city['city']}, TX"
    elif mode == "industry-city":
        url = f"/{industry_slug}-marketing/{city_slug}/"
        path = OUT / f"{industry_slug}-marketing" / city_slug / "index.html"
        h1 = f"Digital Marketing for {industry['industry']} Companies in {city['city']}, TX"
    else:
        url = f"/{service_slug}/{industry_slug}/{city_slug}/"
        path = OUT / service_slug / industry_slug / city_slug / "index.html"
        h1 = f"{service['service']} for {industry['industry']} in {city['city']}, TX"

    title = f"{h1} | Key City Digital"
    desc = f"{service['service']} for {industry['industry']} companies in {city['city']}, TX. Get more calls, better leads, and more booked jobs with Texas-focused contractor marketing systems."

    intro = pick_variant(f"intro:{h1}", INTRO_VARIANTS).format(service=service['service'], city=city['city'], industry=industry['industry'])
    local = pick_variant(f"local:{h1}", LOCAL_VARIANTS).format(
        city=city['city'], metro_area=city['metro_area'], contractor_density=city['contractor_density'], population_tier=city['population_tier'], service=service['service']
    )
    problem = pick_variant(f"problem:{h1}", PROBLEM_VARIANTS).format(city=city['city'], industry=industry['industry'])

    faq_data = load("faqs.json")
    q1 = faq_data["service_faqs"][0]
    q2 = faq_data["industry_faqs"][0]
    q3 = faq_data["city_faqs"][0]
    q2q = q2["q"].format(industry=industry["industry"])
    q2a = q2["a"].format(industry=industry["industry"])
    q3q = q3["q"].format(city=city["city"])
    q3a = q3["a"].format(city=city["city"], population_tier=city["population_tier"], metro_area=city["metro_area"], contractor_density=city["contractor_density"])

    breadcrumb = [
        {"@type":"ListItem","position":1,"name":"Home","item":"https://keycitydigital.com/"},
        {"@type":"ListItem","position":2,"name":service['service'],"item":f"https://keycitydigital.com/services/{service_slug}-contractors/"},
        {"@type":"ListItem","position":3,"name":industry['industry'],"item":"https://keycitydigital.com/industries/"},
        {"@type":"ListItem","position":4,"name":f"{city['city']}, TX","item":f"https://keycitydigital.com{url}"}
    ]

    jsonld = [
        {"@context":"https://schema.org","@type":"WebPage","name":title,"url":f"https://keycitydigital.com{url}","description":desc},
        {"@context":"https://schema.org","@type":"Service","name":service['service'],"serviceType":service['service'],"provider":{"@type":"Organization","name":"Key City Digital"},"areaServed":["Texas",city['city']]},
        {"@context":"https://schema.org","@type":"BreadcrumbList","itemListElement":breadcrumb},
        {"@context":"https://schema.org","@type":"FAQPage","mainEntity":[
            {"@type":"Question","name":q1['q'],"acceptedAnswer":{"@type":"Answer","text":q1['a']}},
            {"@type":"Question","name":q2q,"acceptedAnswer":{"@type":"Answer","text":q2a}},
            {"@type":"Question","name":q3q,"acceptedAnswer":{"@type":"Answer","text":q3a}}
        ]}
    ]

    nearby_links = ""

    html = f"""<!doctype html>
<html lang=\"en\">
<head>
  <meta charset=\"UTF-8\" />
  <meta name=\"viewport\" content=\"width=device-width, initial-scale=1.0\" />
  <title>{title}</title>
  <meta name=\"description\" content=\"{desc}\" />
  <meta property=\"og:type\" content=\"website\" />
  <meta property=\"og:title\" content=\"{title}\" />
  <meta property=\"og:description\" content=\"{desc}\" />
  <meta property=\"og:url\" content=\"https://keycitydigital.com{url}\" />
  <meta name=\"twitter:card\" content=\"summary_large_image\" />
  <meta name=\"twitter:title\" content=\"{title}\" />
  <meta name=\"twitter:description\" content=\"{desc}\" />
  <link rel=\"stylesheet\" href=\"{'../../../../assets/styles.css' if mode=='service-industry-city' else '../../../assets/styles.css'}\" />
  <script type=\"application/ld+json\">{json.dumps(jsonld,separators=(',',':'))}</script>
</head>
<body>
<header><div class=\"container nav-wrap\"><a class=\"brand\" href=\"{'../../../../index.html' if mode=='service-industry-city' else '../../../index.html'}\">KEY CITY <span>DIGITAL</span></a><nav class=\"nav-links\"><a href=\"{'../../../../index.html' if mode=='service-industry-city' else '../../../index.html'}\">Home</a><a href=\"{'../../../../services/index.html' if mode=='service-industry-city' else '../../../services/index.html'}\">Services</a><a href=\"{'../../../../industries.html' if mode=='service-industry-city' else '../../../industries.html'}\">Industries</a><a href=\"{'../../../../resources/index.html' if mode=='service-industry-city' else '../../../resources/index.html'}\">Resources</a><a href=\"{'../../../../contact.html' if mode=='service-industry-city' else '../../../contact.html'}\">Contact</a><a class=\"nav-cta\" href=\"{SCAN}\" target=\"_blank\" rel=\"noopener\">See How Many Jobs You're Losing</a></nav></div></header>
<main>
<section class=\"hero container\"><p class=\"kicker\">Texas Contractor Growth Page</p><h1>{h1}</h1><p class=\"lead\">{intro}</p><div class=\"btn-row\"><a class=\"btn btn-primary\" href=\"{SCAN}\" target=\"_blank\" rel=\"noopener\">Run Free 60-Second Scan</a><a class=\"btn btn-secondary\" href=\"{BOOKING}\" target=\"_blank\" rel=\"noopener\">Book Your Strategy Call</a></div></section>
<section class=\"section-dark\"><div class=\"container grid grid-2\"><article class=\"card\"><h2>Why {service['service']} matters for {industry['industry']} companies in {city['city']}</h2><p>{local}</p><h3>Common local challenges</h3><ul class=\"check\"><li>{problem}</li><li>{city['competitiveness_summary']}</li><li>{city['service_relevance_notes']}</li></ul></article><article class=\"card\"><h2>What Key City Digital delivers</h2><ul class=\"check\">{''.join(f'<li>{d}</li>' for d in service['deliverables'])}</ul><h3>Expected outcomes</h3><ul class=\"check\">{''.join(f'<li>{o}</li>' for o in service['outcomes'])}</ul></article></div></section>
<section><div class=\"container leak-feature\"><h2>Find out how many jobs your website is losing</h2><p class=\"lead\">WebsiteLeakDetector.com is our proprietary diagnostic that shows where leads leak out before they call. Run it first to see your conversion gaps, SEO blockers, and trust breakdowns in under 60 seconds.</p><ul class=\"check\"><li>Identify missed calls caused by weak page flow</li><li>See where homeowners stop before booking</li><li>Get the fastest-fix priorities for more booked jobs</li></ul><div class=\"btn-row\"><a class=\"btn btn-primary\" href=\"{SCAN}\" target=\"_blank\" rel=\"noopener\">See How Many Jobs You're Losing</a><a class=\"btn btn-outline\" href=\"{BOOKING}\" target=\"_blank\" rel=\"noopener\">Book Your Strategy Call</a></div></div></section>
<section class=\"section-dark faq\"><div class=\"container\"><h2>FAQ: {service['service']} for {industry['industry']} in {city['city']}, TX</h2><details><summary>{q1['q']}</summary><p>{q1['a']}</p></details><details><summary>{q2q}</summary><p>{q2a}</p></details><details><summary>{q3q}</summary><p>{q3a}</p></details></div></section>
<section><div class=\"container grid grid-2\"><article class=\"card\"><h2>Related links</h2><ul class=\"check\"><li><a href=\"{'../../../../services/index.html' if mode=='service-industry-city' else '../../../services/index.html'}\">Explore all contractor marketing services</a></li><li><a href=\"{'../../../../industries.html' if mode=='service-industry-city' else '../../../industries.html'}\">See industries we help across Texas</a></li><li><a href=\"{'../../../../resources/index.html' if mode=='service-industry-city' else '../../../resources/index.html'}\">Read contractor growth resources and FAQs</a></li>{nearby_links}</ul><h3>What happens after booking</h3><ul class=\"check\"><li>Get a tailored growth diagnosis for your city + trade</li><li>Receive a 90-day plan focused on calls and booked jobs</li><li>Leave with clear priorities, timeline, and next steps</li></ul></article><article class=\"cta-block\"><h2>Ready to compete harder in {city['city']}?</h2><p class=\"lead\">Get a practical roadmap for calls, leads, and booked jobs based on your service mix and local market realities.</p><div class=\"btn-row\"><a class=\"btn btn-secondary\" href=\"{BOOKING}\" target=\"_blank\" rel=\"noopener\">Book Your Strategy Call</a><a class=\"btn btn-primary\" href=\"{SCAN}\" target=\"_blank\" rel=\"noopener\">See How Many Jobs You're Losing</a></div></article></div></section>
</main>
<footer><div class=\"container\"><p class=\"small\">Generated by Key City Digital programmatic SEO system · Updated {date.today().isoformat()}</p></div></footer>
<script src=\"{'../../../../assets/main.js' if mode=='service-industry-city' else '../../../assets/main.js'}\"></script>
</body>
</html>"""

    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(html)
    return {"url": url, "path": str(path), "priority": 1.0 if city['population_tier']=='large' else 0.7}


def main():
    ap = argparse.ArgumentParser(description="Generate programmatic SEO pages for Key City Digital")
    ap.add_argument("--full", action="store_true", help="Generate full service+industry+city matrix")
    ap.add_argument("--max-pages", type=int, default=150, help="Limit generated pages for safety")
    ap.add_argument("--batch-file", type=str, default="", help="Optional JSON file of explicit page combos")
    ap.add_argument("--clean-output", action="store_true", help="Delete existing pseo HTML files before generation")
    args = ap.parse_args()

    cities = load("cities.json")
    industries = load("industries.json")
    services = load("services.json")

    if args.clean_output and OUT.exists():
        for f in OUT.rglob("*.html"):
            f.unlink()

    generated = []
    # priority first: large cities + core industries
    core_industries = [i for i in industries if i['industry'] in {"Roofing","HVAC","Plumbing","Remodeling","Electrical"}]
    large_cities = [c for c in cities if c['population_tier']=="large"]

    combos = []
    if args.batch_file:
        batch = json.loads(Path(args.batch_file).read_text())
        service_map = {s["slug"]: s for s in services}
        industry_map = {i["slug"]: i for i in industries}
        city_map = {c["slug"]: c for c in cities}
        for item in batch:
            s = service_map[item["service"]]
            i = industry_map[item["industry"]]
            c = city_map[item["city"]]
            combos.append((s, i, c, item.get("mode", "service-industry-city")))

    if not combos:
        for s in services:
            for i in core_industries:
                for c in large_cities:
                    combos.append((s,i,c,"service-industry-city"))

        if args.full:
            for s in services:
                for i in industries:
                    for c in cities:
                        combos.append((s,i,c,"service-industry-city"))

        # secondary patterns
        for s in services:
            for c in cities[:20]:
                combos.append((s, industries[0], c, "service-city"))
        for i in industries[:20]:
            for c in cities[:20]:
                combos.append((services[0], i, c, "industry-city"))

    seen = set()
    for s,i,c,m in combos:
        key=(s['slug'],i['slug'],c['slug'],m)
        if key in seen:
            continue
        seen.add(key)
        generated.append(build_page(s,i,c,m))
        if len(generated) >= args.max_pages:
            break

    # sitemap
    sitemap_lines = ['<?xml version="1.0" encoding="UTF-8"?>','<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">']
    for g in generated:
        sitemap_lines.append(f"  <url><loc>https://keycitydigital.com{g['url']}</loc><changefreq>weekly</changefreq><priority>{g['priority']}</priority></url>")
    sitemap_lines.append('</urlset>')
    (OUT / "sitemap-programmatic.xml").write_text("\n".join(sitemap_lines))

    # indexing strategy manifest
    manifest = {
        "index_now": [g['url'] for g in generated if g['priority'] >= 1.0][:200],
        "defer_index": [g['url'] for g in generated if g['priority'] < 1.0][:500],
        "generated_count": len(generated)
    }
    (OUT / "indexing-strategy.json").write_text(json.dumps(manifest, indent=2))
    print(f"Generated {len(generated)} pages")


if __name__ == "__main__":
    main()
