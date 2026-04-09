# Internal Link Audit & Repair Report

Generated: 2026-04-09

## Broken links found (initial pass)
1. Resource pages linked local pages to `../website-design/...` (missing `/pseo/` path prefix).
2. Programmatic pages included nearby-city links to pages not generated in the current 120-page rollout.
3. `texas-markets.html` was not reachable from the homepage crawl path.
4. Footer/nav link sets were inconsistent across top-level, service, and resource pages.

## Repairs implemented
- Fixed resource local landing page links to `../pseo/{service}/{industry}/{city}-tx/index.html`.
- Removed non-live nearby-city links from generated pSEO pages and replaced with stable links to Services, Industries, and Resources hubs.
- Added Resources and Texas Markets links to nav/footer patterns where missing.
- Upgraded weak hub anchor labels to descriptive text:
  - "Explore the matching service playbook"
  - "See the matching local landing page"

## Validation results
- Broken internal links after repair: **0**
- Merge-conflict markers found (`<<<<<<<`, `=======`, `>>>>>>>`): **0**
- Major crawl-path reachability from homepage:
  - Homepage
  - Services
  - Industries
  - Resources
  - Results
  - Contact
  - About
  - Texas Markets
- Non-pSEO orphan pages: **0**

## Repaired-link examples
- `resources/how-roofers-in-dallas-get-more-leads-online.html`  
  - from: `../website-design/roofing/dallas-tx/index.html`  
  - to: `../pseo/website-design/roofing/dallas-tx/index.html`
- `resources/how-google-maps-ranking-works-for-plumbers.html`  
  - from: `../website-design/plumbing/lubbock-tx/index.html`  
  - to: `../pseo/website-design/plumbing/lubbock-tx/index.html`
- `resources/index.html` hub cards  
  - from: weak anchors (“related service”, “related local page”)  
  - to: descriptive anchors (“Explore the matching service playbook”, “See the matching local landing page”)

## Improved internal linking structure
Homepage -> Services / Industries / Resources / Results / Contact / Texas Markets  
Services -> Resource cluster articles + core conversion pages  
Resources -> Service pages + matching local pSEO pages + results/contact/footer hub links  
pSEO pages -> Services + Industries + Resources + conversion CTAs  
Global footer -> Services / Industries / Results / Texas Markets / Resources / Contact
