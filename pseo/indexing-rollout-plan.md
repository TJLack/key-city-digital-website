# Programmatic SEO Indexing & Scaling Roadmap

Generated on: 2026-04-08  
Current rollout phase: **week1-2**

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
