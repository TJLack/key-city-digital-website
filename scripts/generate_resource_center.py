#!/usr/bin/env python3
import json
from pathlib import Path
from datetime import date

ROOT = Path(__file__).resolve().parents[1]
DATA_FILE = ROOT / "programmatic-seo" / "data" / "resource-articles.json"
OUT = ROOT / "resources"
SCAN = "https://WebsiteLeakDetector.com"
BOOKING = "https://api.leadconnectorhq.com/widget/bookings/digital-marketing-consultation-apykl"

CLUSTER_DESCRIPTIONS = {
    "local-seo-for-contractors": "Ranking systems that grow local visibility for Texas contractors.",
    "website-design-for-contractors": "Conversion-driven website architecture for more booked estimates.",
    "google-maps-ranking": "Google Business Profile and map prominence playbooks.",
    "facebook-ads-for-contractors": "Paid social systems for fast lead generation in Texas markets.",
    "lead-generation-systems": "Full-funnel systems tying traffic to booked revenue."
}


def slug_to_label(slug: str) -> str:
    label = slug.replace("-", " ").title()
    return label.replace("Seo", "SEO").replace("Ai", "AI").replace("Gbp", "GBP")


def make_article(article: dict, all_articles: list[dict]) -> str:
    related = [a for a in all_articles if a["cluster"] == article["cluster"] and a["slug"] != article["slug"]][:3]
    rel_links = "".join([f'<li><a href="{a["slug"]}.html">{a["title"]}</a></li>' for a in related])
    service_link = f'../services/{article["service_slug"]}.html'
    pseo_link = f'../pseo{article["pseo_url"]}index.html'
    city = article["primary_city"].replace("-", " ").title()
    industry = article["industry"].title()

    summary = [
        f"What this means for {industry} teams in {city}",
        "How to apply this in the next 30 days",
        "Which metrics prove the strategy is working",
    ]

    faq_q = [
        f"What is the fastest way {industry.lower()} companies in {city} can improve lead volume?",
        f"How long does this strategy take to influence rankings in {city}?",
    ]

    return f"""<!doctype html>
<html lang=\"en\">
<head>
  <meta charset=\"UTF-8\" />
  <meta name=\"viewport\" content=\"width=device-width, initial-scale=1.0\" />
  <title>{article['title']} | Key City Digital Resources</title>
  <meta name=\"description\" content=\"{article['title']}. Tactical guidance for Texas contractor marketing teams focused on rankings, leads, and booked jobs.\" />
  <link rel=\"stylesheet\" href=\"../assets/styles.css\" />
</head>
<body>
<header><div class=\"container nav-wrap\"><a class=\"brand\" href=\"../index.html\">KEY CITY <span>DIGITAL</span></a><nav class=\"nav-links\"><a href=\"../index.html\">Home</a><a href=\"../services/index.html\">Services</a><a href=\"../industries.html\">Industries</a><a href=\"index.html\">Resources</a><a href=\"../contact.html\">Contact</a><a class=\"nav-cta\" href=\"{SCAN}\" target=\"_blank\" rel=\"noopener\">See How Many Jobs You're Losing</a></nav></div></header>
<main>
<section class=\"hero container\"><p class=\"kicker\">{slug_to_label(article['type'])}</p><h1>{article['title']}</h1><p class=\"lead\">Clear answer: {article['title']} matters because contractor growth comes from tight alignment between local visibility, conversion UX, and lead response speed.</p><div class=\"btn-row\"><a class=\"btn btn-primary\" href=\"{SCAN}\" target=\"_blank\" rel=\"noopener\">Run Free 60-Second Scan</a><a class=\"btn btn-secondary\" href=\"{BOOKING}\" target=\"_blank\" rel=\"noopener\">Book Your Strategy Call</a></div></section>
<section><div class=\"container grid grid-2\"><article class=\"card\"><h2>Definition</h2><p>{article['title']} is a practical operating system for home service marketing in Texas. It combines organic visibility, authority signals, and conversion pathways so clicks become appointments.</p><h3>Quick summary</h3><ul class=\"check\">{''.join(f'<li>{s}</li>' for s in summary)}</ul></article><article class=\"card\"><h2>Where to execute next</h2><ul class=\"check\"><li><a href=\"{service_link}\">Service playbook: {slug_to_label(article['service_slug']).replace('Contractors','for Contractors')}</a></li><li><a href=\"{pseo_link}\">Local landing page: {article['pseo_url']}</a></li><li><a href=\"../services/index.html\">Service hub for Texas contractors</a></li></ul><p>Recommended anchor text example: <em>Local SEO for {industry} contractors in {city}</em>.</p></article></div></section>
<section class=\"section-dark faq\"><div class=\"container\"><h2>FAQ</h2><details><summary>{faq_q[0]}</summary><p>Start with an offer-focused page, local SEO basics, and rapid lead follow-up. In most markets, fixing these three levers produces measurable lift first.</p></details><details><summary>{faq_q[1]}</summary><p>Ranking indicators often move in 4–10 weeks depending on competition and baseline authority. Conversion improvements can happen immediately once page UX and CTA flow are upgraded.</p></details></div></section>
<section><div class=\"container grid grid-2\"><article class=\"card\"><h2>Related resources in this cluster</h2><ul class=\"check\">{rel_links}</ul><h3>Who this strategy call is for</h3><ul class=\"check\"><li>Owners who want more qualified calls, not just traffic</li><li>Teams ready to implement the next 90-day growth plan</li><li>Contractors who want cleaner lead flow and better close rates</li></ul></article><article class=\"cta-block\"><h2>Need a practical rollout plan?</h2><p class=\"lead\">Use WebsiteLeakDetector.com first, then book a strategy session to prioritize traffic, indexing, and conversion changes by impact.</p><div class=\"btn-row\"><a class=\"btn btn-primary\" href=\"{SCAN}\" target=\"_blank\" rel=\"noopener\">See How Many Jobs You're Losing</a><a class=\"btn btn-secondary\" href=\"{BOOKING}\" target=\"_blank\" rel=\"noopener\">Book Your Strategy Call</a></div></article></div></section>
</main>
<footer><div class=\"container\"><p class=\"small\">Resource updated {date.today().isoformat()} · Key City Digital</p></div></footer>
<script src=\"../assets/main.js\"></script>
</body>
</html>
"""


def make_hub(articles: list[dict]) -> str:
    cards = []
    for a in articles:
        cards.append(
            f'<article class="card"><p class="kicker">{slug_to_label(a["cluster"])}</p><h3><a href="{a["slug"]}.html">{a["title"]}</a></h3><p>{slug_to_label(a["type"])} for {a["industry"].title()} teams in {a["primary_city"].replace("-", " ").title()}.</p><p class="small"><a href="../services/{a["service_slug"]}.html">Explore the matching service playbook</a> · <a href="../pseo{a["pseo_url"]}index.html">See the matching local landing page</a></p></article>'
        )

    cluster_blocks = "".join(
        f'<li><strong>{slug_to_label(cluster)}</strong>: {desc}</li>' for cluster, desc in CLUSTER_DESCRIPTIONS.items()
    )

    return f"""<!doctype html>
<html lang=\"en\"><head><meta charset=\"UTF-8\" />
  <meta name=\"viewport\" content=\"width=device-width, initial-scale=1.0\" />
  <title>Contractor Marketing Resources | Key City Digital</title>
  <meta name=\"description\" content=\"Educational resources, strategy breakdowns, local insights, and lead generation guides for Texas contractors.\" />
  <link rel=\"stylesheet\" href=\"../assets/styles.css\" /></head>
<body><header><div class=\"container nav-wrap\"><a class=\"brand\" href=\"../index.html\">KEY CITY <span>DIGITAL</span></a><nav class=\"nav-links\"><a href=\"../index.html\">Home</a><a href=\"../services/index.html\">Services</a><a href=\"../industries.html\">Industries</a><a href=\"index.html\">Resources</a><a href=\"../contact.html\">Contact</a><a class=\"nav-cta\" href=\"{SCAN}\" target=\"_blank\" rel=\"noopener\">See How Many Jobs You're Losing</a></nav></div></header>
<main><section class=\"hero container\"><p class=\"kicker\">Resource Center</p><h1>Texas Contractor Marketing Resource Library</h1><p class=\"lead\">A supporting content layer built to accelerate rankings, indexing, authority, traffic, and booked jobs across Texas home service markets.</p><div class=\"btn-row\"><a class=\"btn btn-primary\" href=\"{SCAN}\" target=\"_blank\" rel=\"noopener\">Run Free 60-Second Scan</a><a class=\"btn btn-secondary\" href=\"{BOOKING}\" target=\"_blank\" rel=\"noopener\">Book Your Strategy Call</a></div></section>
<section class=\"section-dark\"><div class=\"container\"><h2>Authority clusters</h2><ul class=\"check\">{cluster_blocks}</ul></div></section>
<section><div class=\"container grid grid-3">{''.join(cards)}</div></section></main>
<footer><div class=\"container\"><p class=\"small\">{len(articles)} published/planned resources · Updated {date.today().isoformat()}</p></div></footer>
<script src=\"../assets/main.js\"></script></body></html>
"""


def main() -> None:
    articles = json.loads(DATA_FILE.read_text())
    OUT.mkdir(parents=True, exist_ok=True)
    (OUT / "index.html").write_text(make_hub(articles))
    for article in articles:
        (OUT / f"{article['slug']}.html").write_text(make_article(article, articles))

    cluster_map = {}
    for article in articles:
        cluster_map.setdefault(article["cluster"], []).append({
            "title": article["title"],
            "slug": article["slug"],
            "service_link": f"/services/{article['service_slug']}.html",
            "local_page_link": article["pseo_url"],
            "type": article["type"],
        })

    outputs = {
        "generated_on": date.today().isoformat(),
        "total_articles": len(articles),
        "clusters": cluster_map,
    }
    (ROOT / "pseo" / "authority-cluster-map.json").write_text(json.dumps(outputs, indent=2))
    print(f"Generated {len(articles)} resource articles")


if __name__ == "__main__":
    main()
