# Google Analytics & Search Console Improvement Skill

[中文文档](README_CN.md)

An AI agent skill that performs goal-driven website analysis — collecting data from Google Search Console and GA4, auditing SEO/GEO readiness, and generating prioritized improvement plans with data visualization.

## What It Does

Give your AI agent a website URL, and it will:

1. **Understand your website goals** — visit the site, define the intended user journey
2. **Collect search & analytics data** — via GSC and GA4 APIs (or manual CSV export)
3. **Analyze where users diverge** — map search queries and user behavior against your goals
4. **Audit the live site** — SEO metadata, GEO (AI search) readiness, performance, security
5. **Generate a prioritized report** — P0-P3 action items with charts, execution roadmap

### Core Principle

**Goal → Data → Gap → Action**

Every analysis starts from what your site wants users to do. The skill finds where reality diverges from intention and tells you exactly what to fix.

## Installation

```bash
npx skills add morvanzhou/data-driven-product
```

## Quick Start

Tell your AI agent:

> Analyze example.com using the data-driven-product skill

The agent will guide you through setup and run the full analysis automatically.

### Data Collection Modes

| Mode | Setup | Best For |
|------|-------|----------|
| **API auto-collect** (recommended) | Google Cloud Service Account (~10 min first time) | Full analysis with all data |
| **Manual CSV export** | None | Quick analysis with exported data |
| **Browser audit only** | None | Technical SEO/GEO audit without analytics data |

### API Setup (Mode A)

1. Create a Google Cloud project, enable **Search Console API**, **Analytics Data API**, and **PageSpeed Insights API**
2. Create a Service Account and download the JSON key
3. Grant access: add the SA email as viewer in both GSC and GA4
4. Tell the agent your key file path, GSC site URL, and GA4 Property ID

> **Tip**: GSC has two property types — Domain (`sc-domain:example.com`) and URL-prefix (`https://example.com`). Using the wrong format causes a 403 error.

See [references/gsc-api-guide.md](skills/data-driven-product/references/gsc-api-guide.md) for detailed setup instructions.

## Analysis Workflow

```
Phase 0  →  Website reconnaissance & goal definition
Phase 1  →  Data collection (API / CSV / browser-only)
Phase 2  →  Search performance analysis (GSC)
Phase 3  →  User behavior analysis (GA4)
Phase 3b →  Funnel exploration (optional, custom events)
Phase 4  →  Live site audit (performance, SEO, security)
Phase 5  →  Source code review (optional)
Phase 5b →  SEO & GEO optimization checklist
Phase 6  →  Goal-aligned improvement report with charts
```

## Output

The skill generates a full set of analysis reports and charts in `.skills-data/data-driven-product/`:

- **`analysis/improvement-report.md`** — Final report with executive summary, goal achievement status, P0-P3 prioritized actions, and execution roadmap
- **`analysis/`** — Phase-by-phase detailed reports (search analysis, behavior analysis, funnel analysis, site audit, SEO/GEO checklist)
- **`charts/`** — Data visualization charts (PNG) embedded in reports

## Companion Skills

| Skill | Use Case |
|-------|----------|
| `seo-geo` | Implement SEO/GEO recommendations from the report |
| `agent-browser` | Browser automation for site auditing |
| `frontend-design` | Implement frontend/UX improvements |

## License

MIT
