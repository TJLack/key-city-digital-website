# Full QA & Repair Report (Launch-Clean Pass)

## Issues found by page/group

### Global (sitewide)
1. CTA wording inconsistent and occasionally generic.
2. Multiple pages linked consultation CTAs to contact page instead of direct booking calendar.
3. Navigation/footer link sets inconsistent (resources link missing on several pages).
4. Broken internal links in resources and pSEO related-link blocks.
5. Weak anchor labels in resources hub (generic "related service" style).

### Homepage (`index.html`)
1. WebsiteLeakDetector positioning not explicit enough as proprietary diagnostic.
2. Mid-page booking CTA pointed to contact page in one section.

### Contact page (`contact.html`)
1. Booking section lacked trust framing and expectation-setting detail.
2. Form submit microcopy was weak and non-outcome-driven.
3. Objection handling FAQ needed stronger skepticism/cost/timeline reassurance.

### Service pages (`services/*.html`)
1. Consultation CTA destinations inconsistent (contact page vs booking widget).
2. Nav/footer link consistency gaps.

### Resource pages (`resources/*.html`)
1. Local-page links pointed to wrong path root (missing `/pseo/`).
2. Hub card anchor text was generic and less descriptive.

### Programmatic pages (`pseo/website-design/*/*/index.html`)
1. Nearby-city links referenced pages not generated in the current rollout, creating broken links.
2. Nav lacked direct resource-center link.

## Repairs implemented
- Standardized conversion CTA language sitewide.
- Routed high-intent CTA actions to booking widget where appropriate.
- Improved Homepage + Contact page conversion framing and trust copy.
- Added/normalized Resources link in nav/footer patterns.
- Fixed resource local-link paths to `/pseo/...`.
- Removed broken nearby-city links from generated pSEO pages and replaced with strong internal links.
- Added resource-center links inside pSEO related links.
- Regenerated resources + pSEO pages and re-applied indexing strategy controls.
- Re-ran structural QA checks (links, metadata, CTA presence, nav/footer presence).

## Validation checks run
- Link integrity check across all HTML files (0 missing internal links).
- Metadata/nav/footer/dual-CTA structural scan across all HTML files (0 issues).
- Python compile check for generation/strategy scripts.

