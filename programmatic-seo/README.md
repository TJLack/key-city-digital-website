# Key City Digital Programmatic SEO System

This system generates scalable, high-quality, conversion-focused pages for:

- `/{service}/{industry}/{city}-tx/`
- `/{service}/{city}-tx/`
- `/{industry}-marketing/{city}-tx/`

## Data Sources

- `programmatic-seo/data/cities.json`
- `programmatic-seo/data/industries.json`
- `programmatic-seo/data/services.json`
- `programmatic-seo/data/faqs.json`
- `programmatic-seo/data/internalLinks.json`

## Generate Pages

```bash
python scripts/generate_programmatic_seo.py --max-pages 120
```

To generate broader coverage:

```bash
python scripts/generate_programmatic_seo.py --full --max-pages 5000
```

## Output

Generated pages are written to `pseo/` and include:

- unique H1/H2/H3 structure
- meta title + description
- Open Graph + Twitter tags
- JSON-LD schema (WebPage, Service, FAQ, Breadcrumb)
- conversion CTAs to `WebsiteLeakDetector.com` and booking calendar
- internal links and related-page blocks

Additional artifacts:

- `pseo/sitemap-programmatic.xml`
- `pseo/indexing-strategy.json`
- `pseo/tier-classification.json`
- `pseo/indexing-rollout-plan.md`
- `pseo/sitemap-core.xml`
- `pseo/sitemap-tier1.xml`
- `pseo/sitemap-tier2.xml`

## Indexing + Scaling Controls

Apply controlled rollout rules to generated pages:

```bash
python scripts/apply_indexing_strategy.py --phase week1-2
```

Phase options:
- `week1-2`: index Tier 1 only
- `week3-4`: unlock top 30% Tier 2 pages
- `month2`: unlock top 65% Tier 2 pages
- `month3-plus`: unlock all Tier 2 pages and start Tier 3 promotion

The strategy script updates:
- per-page robots directives (`index/follow`, `noindex/follow`, `noindex/nofollow`)
- tier classifications for every generated page
- segmented sitemaps for progressive indexing
- rollout + monitoring manifests for scaling decisions

## Resource/Authority Layer

Generate the supporting content hub and article pages:

```bash
python scripts/generate_resource_center.py
```

This builds `resources/index.html` plus article pages that:
- reinforce service + local programmatic pages with contextual links
- include AI-friendly definitions, summaries, and FAQ blocks
- include both conversion CTAs (`WebsiteLeakDetector.com` + booking widget)
