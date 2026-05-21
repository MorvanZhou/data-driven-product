---
name: data-driven-product
description: Data-driven product analysis and iteration decision tool. Collects data via GA4, GSC, Bing Webmaster, and Microsoft Clarity to provide pre-analysis (product/direction selection), post-analysis (optimize existing products), and decision analysis (upgrade or abandon), outputting interactive HTML reports.
---

# Data-Driven Product Analysis and Iteration Decisions

Through multi-source data collection and analysis, answer three core questions:
1. **What to build** (Pre-Analysis) — Market demand, competitor reverse-engineering, search intent gaps
2. **How to optimize** (Post-Analysis) — Page health, user paths, funnel diagnosis, UX quality
3. **Upgrade or abandon** (Decision Analysis) — Lifecycle assessment, ROI comparison, abandonment signals

The deliverable is an **interactive HTML report** rendered with ECharts data charts, viewable directly in a browser.

---

## Data Storage

All runtime data is stored in `$DATA_DIR`, separated from the skill code.

```
<project_root>/.skills-data/data-driven-product/
  .env        # Configuration (auth, URLs, etc.), auto-loaded by scripts
  data/       # Raw data: API response JSON
  analysis/   # Intermediate analysis results JSON (script output)
  reports/    # Final HTML reports (human-readable deliverables)
  scripts/    # Analysis scripts
  configs/    # Service Account JSON keys, API tokens
  cache/      # API cache
  tmp/        # Screenshots and temporary files
  venv/       # Python virtual environment (managed by uv)
```

**Directory separation principle**:
- `data/` = Raw API responses (input)
- `analysis/` = Structured analysis results JSON processed by scripts (intermediate)
- `reports/` = Final HTML reports (deliverables, for human consumption)
- `scripts/` = Analysis code

---

## Core Principles

### Data-Driven Decisions

All analysis must be data-based, processing raw data with code to produce verifiable conclusions. Analysis conclusions must directly point to action decisions (build/don't build/optimize/abandon).

### Code-Driven Analysis

**All data analysis must be done through code execution — never manually read JSON and summarize.**

1. Write Python scripts in `$DATA_DIR/scripts/` to read raw JSON
2. Execute scripts to output structured analysis results to `$DATA_DIR/analysis/`
3. Use analysis results to generate HTML reports to `$DATA_DIR/reports/`

### HTML + ECharts Reports

Deliverables are self-contained HTML files, loading ECharts via CDN:
- Interactive charts (hover tooltips, zoom, responsive)
- Single file can be opened directly in a browser
- Chart data embedded in HTML `<script>` tags

Detailed specifications in [references/data-visualization-guide.md](references/data-visualization-guide.md).

---

## Data Sources

| Tool | Data Provided | Configuration Guide |
|------|--------------|-------------------|
| **Google Search Console** | Search query rankings, CTR, impressions, index status | [setup/gsc-setup.md](references/setup/gsc-setup.md) |
| **Google Analytics 4** | Traffic, user behavior, conversion funnels, user profiles | [setup/ga4-setup.md](references/setup/ga4-setup.md) |
| **Bing Webmaster Tools** | Bing search data, keyword research, backlinks, crawl status | [setup/bing-webmaster-setup.md](references/setup/bing-webmaster-setup.md) |
| **Microsoft Clarity** | UX quality signals: rage clicks, dead clicks, scroll depth, quick backs | [setup/clarity-setup.md](references/setup/clarity-setup.md) |

### .env Configuration Summary

```bash
SITE_URL=https://example.com
GSC_SITE_URL=sc-domain:example.com
GA4_PROPERTY_ID=123456789
BING_WEBMASTER_API_KEY=xxx
CLARITY_API_TOKEN=xxx
PSI_API_KEY=              # Optional, rate-limited without it
SOURCE_CODE_PATH=         # Optional, source code path
```

---

## Analysis Framework

### Pre-Analysis — Deciding "What to Build"

Used for product selection, direction choosing, and evaluating whether to build a product/page.

| ID | Analysis Module | Core Question | Primary Data Source |
|----|----------------|--------------|-------------------|
| **P1** | Keyword Market Demand Analysis | How large is search demand in a given area? Growth trends? | GSC trends + Bing keyword |
| **P2** | Competitor Traffic Reverse-Engineering | What keywords drive competitor traffic? Which keywords am I missing? | Bing related_keywords + GSC comparison |
| **P3** | Search Intent Gap Analysis | What are users searching for that lacks good solutions? | GSC queries + Bing keyword + search result audit |
| **P4** | Content/Product Opportunity Assessment | What's the expected ROI of building this? | Search volume × estimated CTR × conversion rate |
| **P5** | User Need Clustering | Cluster core need groups from search queries | GSC queries clustering |

#### P1: Keyword Market Demand Analysis

> **Purpose**: Assess the search demand scale and growth trends in a given area to provide market capacity data for product selection.

**Data Collection**:
```bash
# GSC trend data (existing keywords)
python scripts/gsc_query.py --dimensions date,query --limit 5000 -o "$DATA_DIR/data/gsc_query_trends.json"

# Bing keyword research (new keyword discovery)
python scripts/bing_query.py --mode keyword --query "target keyword" --country us -o "$DATA_DIR/data/bing_keyword.json"
python scripts/bing_query.py --mode related_keywords --query "target keyword" --country us -o "$DATA_DIR/data/bing_related.json"
```

**Analysis Script Output**:
- Keyword search volume trends (monthly/quarterly)
- Total TAM (Total Addressable Market) of keyword clusters
- Growth/decline trend assessment
- Seasonality identification

**Output**: `$DATA_DIR/analysis/market_demand.json`

#### P2: Competitor Traffic Reverse-Engineering

> **Purpose**: Reverse-engineer competitor strategies through search data to discover uncovered keyword spaces.

**Data Collection**:
```bash
# Own keyword coverage
python scripts/gsc_query.py --dimensions query --limit 5000 -o "$DATA_DIR/data/gsc_all_queries.json"

# Bing related keywords (expand perspective)
python scripts/bing_query.py --mode related_keywords --query "core keyword" --country us -o "$DATA_DIR/data/bing_related.json"
```

**Analysis Script Output**:
- Own keyword coverage vs Bing-recommended related terms → coverage gaps
- Search volume ranking of uncovered keywords
- Opportunity priority scoring

**Output**: `$DATA_DIR/analysis/competitor_gaps.json`

#### P3: Search Intent Gap Analysis

> **Purpose**: Identify areas with strong search demand but poor existing solutions.

**Data Collection**: Same as P1 + P2 data, plus auditing search result page quality via `agent-browser`.

**Analysis Dimensions**:
- High search volume + poor search result quality (informational content dominates, few tools)
- Clear search intent but dispersed CTR (no clear winner)
- Long-tail keyword clusters with no dedicated product coverage

**Output**: `$DATA_DIR/analysis/intent_gaps.json`

#### P4: Content/Product Opportunity Assessment

> **Purpose**: Quantify the expected return of building a product/page.

**Calculation Model**:
```
Expected monthly traffic = Keyword monthly search volume × Estimated CTR (based on ranking position)
Expected conversions = Expected monthly traffic × Industry average conversion rate
ROI score = Expected conversions / Implementation difficulty (keyword competition)
```

**Output**: `$DATA_DIR/analysis/opportunity_scoring.json`

#### P5: User Need Clustering

> **Purpose**: Automatically cluster core need groups from search queries to guide product line planning.

**Data Collection**:
```bash
python scripts/gsc_query.py --dimensions query --limit 5000 -o "$DATA_DIR/data/gsc_all_queries.json"
```

**Analysis Methods**:
- Cluster search terms by semantic similarity
- Classify by user intent stage (informational/comparison/purchase/usage)
- Map to product features

**Output**: `$DATA_DIR/analysis/need_clusters.json`

---

### Post-Analysis — Deciding "How to Optimize"

Used for iterative optimization of existing products/pages.

| ID | Analysis Module | Core Question | Primary Data Source |
|----|----------------|--------------|-------------------|
| **A1** | Page Health Assessment | How is each page performing? Worth investing or should be abandoned? | GA4 pages + GSC pages + Clarity URL |
| **A2** | User Behavior Path Analysis | How do users actually use the product? Where do they get stuck/leave? | GA4 behavior + Clarity rage/dead clicks |
| **A3** | Conversion Funnel Diagnosis | How much is lost at each step? Why? | GA4 funnel + Clarity |
| **A4** | Traffic Channel ROI | Which channel has the highest quality users? | GA4 acquisition + conversion |
| **A5** | Device/Geo Differential Analysis | Is mobile dragging performance down? Which markets deserve more investment? | GA4 device/geo + GSC device/country |
| **A6** | Content Decay Monitoring | Which previously good pages are declining? | GSC trends comparison |
| **A7** | SEO/GEO Technical Health | Are technical issues blocking growth? | seo_audit + geo_audit + perf_audit |
| **A8** | User Persona Analysis | Who are the users? How do different groups behave differently? | GA4 demographics + Clarity segments |

#### A1: Page Health Assessment

> **Purpose**: Score each page to determine which are worth optimizing, which should be merged or deleted.

**Data Collection**:
```bash
python scripts/ga4_query.py --preset top_pages --limit 200 -o "$DATA_DIR/data/ga4_pages.json"
python scripts/gsc_query.py --dimensions page --limit 500 -o "$DATA_DIR/data/gsc_pages.json"
python scripts/clarity_query.py --days 3 --dimension URL -o "$DATA_DIR/data/clarity_urls.json"
```

**Health Score Dimensions**:
- Traffic (GA4 sessions + GSC clicks)
- User satisfaction (bounce rate + Clarity rage/dead clicks + scroll depth)
- Search performance (GSC impressions + CTR + position)
- Conversion contribution (GA4 conversions)

**Output**: `$DATA_DIR/analysis/page_health.json`

#### A2: User Behavior Path Analysis

> **Purpose**: Understand how users actually use the product and discover UX friction points.

**Data Collection**:
```bash
python scripts/ga4_query.py --preset user_behavior --limit 200 -o "$DATA_DIR/data/ga4_behavior.json"
python scripts/ga4_query.py --preset landing_pages --limit 100 -o "$DATA_DIR/data/ga4_landing.json"
python scripts/clarity_query.py --days 3 --dimension URL -o "$DATA_DIR/data/clarity_urls.json"
```

**Analysis Dimensions**:
- Landing page → next step path (whether it matches design intent)
- High-traffic page engagement rate
- Pages with concentrated Clarity rage clicks / dead clicks
- Relationship between scroll depth and content length

**Output**: `$DATA_DIR/analysis/user_paths.json`

#### A3: Conversion Funnel Diagnosis

> **Purpose**: Quantify conversion loss at each step and locate bottlenecks.

**Data Collection**:
```bash
python scripts/ga4_funnel.py --steps "event1,event2,event3" -o "$DATA_DIR/data/ga4_funnel.json"
python scripts/ga4_funnel.py --steps "event1,event2,event3" --breakdown deviceCategory -o "$DATA_DIR/data/ga4_funnel_device.json"
python scripts/clarity_query.py --days 3 -o "$DATA_DIR/data/clarity_overview.json"
```

**Analysis Dimensions**:
- Completion rate and drop-off rate at each step
- Funnel differences across devices/channels
- Correlation between Clarity quick backs and funnel abandonment

**Output**: `$DATA_DIR/analysis/funnel_diagnosis.json`

#### A4: Traffic Channel ROI

> **Purpose**: Quantify user quality from each channel to guide traffic investment decisions.

**Data Collection**:
```bash
python scripts/ga4_query.py --preset user_acquisition -o "$DATA_DIR/data/ga4_acquisition.json"
python scripts/ga4_query.py --preset conversion_events -o "$DATA_DIR/data/ga4_conversions.json"
python scripts/clarity_query.py --days 3 --dimension Channel -o "$DATA_DIR/data/clarity_channel.json"
```

**Analysis Dimensions**:
- Sessions, engagement rate, conversion rate per channel
- Clarity UX quality of channel users (rage/dead click ratios)
- Channel ROI ranking

**Output**: `$DATA_DIR/analysis/channel_roi.json`

#### A5: Device/Geo Differential Analysis

> **Purpose**: Discover experience shortcomings and opportunity markets across device and geography dimensions.

**Data Collection**:
```bash
python scripts/ga4_query.py --preset device_breakdown -o "$DATA_DIR/data/ga4_devices.json"
python scripts/ga4_query.py --preset geo_distribution -o "$DATA_DIR/data/ga4_geo.json"
python scripts/gsc_query.py --dimensions device,country -o "$DATA_DIR/data/gsc_devices.json"
python scripts/clarity_query.py --days 3 --dimension Device -o "$DATA_DIR/data/clarity_device.json"
python scripts/clarity_query.py --days 3 --dimension Country -o "$DATA_DIR/data/clarity_country.json"
```

**Analysis Dimensions**:
- Core metric differences between mobile vs desktop
- Asymmetry between geo traffic and conversion rate (high traffic + low conversion = experience issues)
- Device-specific Clarity UX problems

**Output**: `$DATA_DIR/analysis/device_geo_analysis.json`

#### A6: Content Decay Monitoring

> **Purpose**: Detect declining pages early and decide whether to update or abandon them.

**Data Collection**:
```bash
# Last 28 days vs previous 28 days
python scripts/gsc_query.py --dimensions page --start-date 28daysAgo --end-date yesterday -o "$DATA_DIR/data/gsc_pages_recent.json"
python scripts/gsc_query.py --dimensions page --start-date 56daysAgo --end-date 29daysAgo -o "$DATA_DIR/data/gsc_pages_previous.json"
python scripts/gsc_query.py --dimensions date,page --limit 5000 -o "$DATA_DIR/data/gsc_page_trends.json"
```

**Analysis Dimensions**:
- Period-over-period traffic change (clicks/impressions decline magnitude)
- Ranking changes (position increase = decline)
- Decay speed and duration

**Output**: `$DATA_DIR/analysis/content_decay.json`

#### A7: SEO/GEO Technical Health

> **Purpose**: Check whether technical issues are blocking growth.

**Data Collection**:
```bash
source "$DATA_DIR/venv/bin/activate"
set -a; source "$DATA_DIR/.env"; set +a
python scripts/seo_audit.py --url "$SITE_URL" --sitemap -o "$DATA_DIR/analysis/seo_audit.json"
python scripts/geo_audit.py --url "$SITE_URL" --sitemap -o "$DATA_DIR/analysis/geo_audit.json"
python scripts/perf_audit.py --url "$SITE_URL" --sitemap -o "$DATA_DIR/analysis/perf_audit.json"
```

Refer to the checklist in [references/SEO-GEO-Optimization-Checklist.md](references/SEO-GEO-Optimization-Checklist.md).

**Output**: `$DATA_DIR/analysis/tech_health.json`

#### A8: User Persona Analysis

> **Purpose**: Understand user group characteristics to provide audience perspective for product iteration.

**Data Collection**:
```bash
python scripts/ga4_query.py --preset demographics_age -o "$DATA_DIR/data/ga4_age.json"
python scripts/ga4_query.py --preset demographics_gender -o "$DATA_DIR/data/ga4_gender.json"
python scripts/ga4_query.py --preset demographics_geo -o "$DATA_DIR/data/ga4_demo_geo.json"
python scripts/ga4_query.py --preset demographics_language -o "$DATA_DIR/data/ga4_language.json"
python scripts/ga4_query.py --preset new_vs_returning -o "$DATA_DIR/data/ga4_new_returning.json"
python scripts/clarity_query.py --days 3 --dimension Device --dimension2 Country -o "$DATA_DIR/data/clarity_demo.json"
```

Full methodology in [references/user-persona-analysis-reference.md](references/user-persona-analysis-reference.md).

**Output**: `$DATA_DIR/analysis/user_personas.json`

---

### Decision Analysis — Upgrade or Abandon?

| ID | Analysis Module | Core Question | Primary Data Source |
|----|----------------|--------------|-------------------|
| **D1** | Product Lifecycle Assessment | Growth phase, plateau, or decline? | GSC trends + GA4 trends (90-day line) |
| **D2** | ROI Comparison | Optimize existing vs build new — which yields better returns? | Existing data ceiling + new keyword TAM |
| **D3** | Abandonment Signal Detection | Under what conditions should we abandon? | Multi-signal composite judgment |

#### D1: Product Lifecycle Assessment

> **Purpose**: Determine what phase a product/page is in to guide resource allocation.

**Data Collection**:
```bash
python scripts/gsc_query.py --dimensions date --start-date 90daysAgo -o "$DATA_DIR/data/gsc_90d_trends.json"
python scripts/ga4_query.py --preset traffic_overview --start-date 90daysAgo -o "$DATA_DIR/data/ga4_90d_traffic.json"
```

**Assessment Criteria**:
- **Growth phase**: clicks/sessions continuously rising, position continuously declining (ranking improving)
- **Plateau phase**: metrics stable, no obvious upward/downward trend
- **Decline phase**: clicks continuously declining > 4 weeks, position rising

**Output**: `$DATA_DIR/analysis/lifecycle.json`

#### D2: ROI Comparison

> **Purpose**: Quantify the ROI of "optimizing existing pages" vs "building something new."

**Analysis Model**:
```
Expected benefit of optimization = Current traffic × (Estimated post-optimization CTR - Current CTR) × Conversion rate
Expected benefit of new build = New keyword search volume × Estimated CTR × Conversion rate
Decision = max(Optimization benefit/Optimization cost, New build benefit/New build cost)
```

**Output**: `$DATA_DIR/analysis/roi_comparison.json`

#### D3: Abandonment Signal Detection

> **Purpose**: Clearly define under what conditions a product/page should be abandoned.

**Abandonment Signals** (recommend abandoning if 3+ are met):
- GSC impressions declining for 8 consecutive weeks
- GA4 sessions < 10/week with no growth trend
- Clarity rage click rate > 20% (extreme user frustration)
- Search demand shrinking (overall decline in related keyword search volume)
- Rankings continuously dropping with no recovery through content updates
- Zero conversion rate for 4+ consecutive weeks

**Output**: `$DATA_DIR/analysis/abandon_signals.json`

---

## Workflow

```
Pre-check →  Run check_config.py to verify data source readiness
Phase 0   →  Website Reconnaissance & Goal Definition
Phase 1   →  Data Source Configuration & Data Collection
Phase 2   →  Select and Execute Analysis Modules (P/A/D combinations)
Phase 3   →  Generate HTML Report
```

### Pre-check: Verify Data Source Configuration

> **Rule**: Before executing any user task, ALWAYS run `check_config.py` first to determine which data sources are configured and available.

```bash
source "$DATA_DIR/venv/bin/activate"
python scripts/check_config.py
```

Based on the output:
1. **Identify which tools are ready** — only use configured data sources for subsequent analysis
2. **If the task requires a missing source** — inform the user what's not configured and guide them to set it up (refer to the setup guides), or proceed with available sources only
3. **Proceed with available tools** — adapt the analysis plan to use only the confirmed-ready data sources

This ensures no script fails due to missing credentials and the analysis scope matches actual capabilities.

### Phase 0: Website Reconnaissance & Goal Definition

> **Purpose**: Understand what the product does, who the target users are, and the core conversion path.

1. Use `agent-browser` to visit the website, take screenshots + extract metadata
2. Classify website type (SaaS/e-commerce/content/tool, etc.)
3. Infer goals and confirm with user
4. Based on user needs, determine which analysis module combinations to execute

Save to `$DATA_DIR/analysis/website-profile.json`.

Detailed operations in [references/website-reconnaissance-reference.md](references/website-reconnaissance-reference.md).

### Phase 1: Data Source Configuration & Data Collection

**1a. Initialize directories & Python environment**:
```bash
DATA_DIR=".skills-data/data-driven-product"
mkdir -p "$DATA_DIR"/{data,analysis,reports,scripts,cache,tmp,configs}
```

Set up Python 3.12 virtual environment (first time):
```bash
uv venv "$DATA_DIR/venv" --python 3.12
uv pip install -p "$DATA_DIR/venv" -r skills/data-driven-product/scripts/pyproject.toml
```

> **Important**: All Python script execution must first activate the venv:
> ```bash
> source "$DATA_DIR/venv/bin/activate"
> python scripts/xxx.py ...
> ```

**1b. Configure data sources**:

Guide users to configure as needed (refer to setup guides):
- GSC → [setup/gsc-setup.md](references/setup/gsc-setup.md)
- GA4 → [setup/ga4-setup.md](references/setup/ga4-setup.md)
- Bing → [setup/bing-webmaster-setup.md](references/setup/bing-webmaster-setup.md)
- Clarity → [setup/clarity-setup.md](references/setup/clarity-setup.md)

**1c. Batch data collection**:

Based on the analysis modules determined in Phase 0, execute the corresponding data collection commands (see the "Data Collection" section of each analysis module).

**Data Collection Modes**:

| Mode | Description | Use Case |
|------|-------------|----------|
| **A. Automated API** | Configure Service Account / API Key, scripts collect automatically | Most complete data, recommended |
| **B. Manual CSV Export** | User exports CSV from GA4/GSC console | Zero configuration |
| **C. Browser Audit Only** | Direct website access, no analytics data | Quick technical check |

**Mode B: CSV Export Guide**:
- GSC: [Search Console](https://search.google.com/search-console/) → Select site → "Search results" → Set last 3 months → Export CSV → `$DATA_DIR/data/gsc_export.csv`
- GA4: [Google Analytics](https://analytics.google.com/) → Export "Pages and screens" → `$DATA_DIR/data/ga4_pages.csv`; "Traffic acquisition" → `$DATA_DIR/data/ga4_acquisition.csv`; "Landing pages" → `$DATA_DIR/data/ga4_landing.csv`

**PageSpeed Insights (direct curl)**:
```bash
PSI_BASE="https://www.googleapis.com/pagespeedonline/v5/runPagespeed?url=$SITE_URL&category=PERFORMANCE&category=SEO&category=ACCESSIBILITY&category=BEST_PRACTICES"
PSI_KEY_PARAM="${PSI_API_KEY:+&key=$PSI_API_KEY}"
curl -s "${PSI_BASE}&strategy=mobile${PSI_KEY_PARAM}" > "$DATA_DIR/data/psi_mobile.json"
curl -s "${PSI_BASE}&strategy=desktop${PSI_KEY_PARAM}" > "$DATA_DIR/data/psi_desktop.json"
```

**Clarity collection strategy** (10 req/day, 1-3 day window):
- Always use `--days 3` for maximum data
- Dimension priority: URL > Device > Source > Country
- For long-term trends, archive every 3 days to `$DATA_DIR/cache/`

**GSC advanced query scenarios**: section analysis (page path filter), keyword trend tracking (`query` + `date` + page filter), long-tail discovery (high rowLimit), regex matching (`includingRegex` operator). Advanced filtering requires custom scripts using `dimensionFilterGroups`.

**GSC API capabilities**: up to 3 dimensions, 16-month date range, 25,000 rows per request, `dataState: 'all'` for fresh data.

**GA4 common dimensions**: `date`, `pagePath`, `pageTitle`, `landingPage`, `sessionDefaultChannelGroup`, `sessionSource`, `sessionMedium`, `deviceCategory`, `country`, `city`, `eventName`.

**GA4 common metrics**: `sessions`, `totalUsers`, `newUsers`, `screenPageViews`, `bounceRate`, `averageSessionDuration`, `engagementRate`, `eventCount`, `conversions`.

### Phase 2: Execute Analysis

Based on the analysis modules selected in Phase 0, write analysis scripts to process raw data:

1. Write Python scripts in `$DATA_DIR/scripts/`
2. Scripts read from `$DATA_DIR/data/*.json`
3. Scripts output structured analysis results to `$DATA_DIR/analysis/*.json`

Each analysis module's script should output a JSON containing:
- `summary`: Core findings summary
- `data`: Processed data (for chart rendering)
- `recommendations`: Action recommendations
- `charts`: Chart configurations (array of ECharts option objects)

### Phase 3: Generate HTML Report

Aggregate all analysis results into a self-contained HTML report:

1. Read `$DATA_DIR/analysis/*.json`
2. Assemble ECharts chart configurations
3. Generate HTML using report template
4. Save to `$DATA_DIR/reports/report.html`

Report template and generation specifications in [references/report-template.md](references/report-template.md).
Chart specifications in [references/data-visualization-guide.md](references/data-visualization-guide.md).

---

## Reference Documents

| Document | Content |
|----------|---------|
| [references/setup/gsc-setup.md](references/setup/gsc-setup.md) | GSC configuration + script usage |
| [references/setup/ga4-setup.md](references/setup/ga4-setup.md) | GA4 configuration + script usage |
| [references/setup/bing-webmaster-setup.md](references/setup/bing-webmaster-setup.md) | Bing Webmaster configuration + script usage |
| [references/setup/clarity-setup.md](references/setup/clarity-setup.md) | Microsoft Clarity configuration + script usage |
| [references/data-visualization-guide.md](references/data-visualization-guide.md) | ECharts chart specifications, chart type selection, report generation patterns |
| [references/report-template.md](references/report-template.md) | HTML report template |
| [references/metrics-glossary.md](references/metrics-glossary.md) | Metric thresholds, diagnostic criteria, priority matrix |
| [references/SEO-GEO-Optimization-Checklist.md](references/SEO-GEO-Optimization-Checklist.md) | SEO & GEO audit checklist |
| [references/website-reconnaissance-reference.md](references/website-reconnaissance-reference.md) | Website reconnaissance operations guide |
| [references/user-persona-analysis-reference.md](references/user-persona-analysis-reference.md) | User persona analysis methodology |

## Auxiliary Skills

- SEO implementation → `seo-geo`
- Browser automation → `agent-browser`
- Frontend redesign → `frontend-design`
