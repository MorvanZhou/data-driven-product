# Key Metrics and Analysis Dimensions

## Analysis Dimensions

---

### 7. UX Quality (Microsoft Clarity)

**Primary data source**: Clarity Data Export API

| Metric | Healthy Range | Warning Signal |
|--------|---------------|----------------|
| Rage Click Rate | < 3% sessions | > 5% severe UX issues |
| Dead Click Rate | < 5% sessions | > 10% clickability issues |
| Quick Back Rate | < 10% | > 20% landing page doesn't meet expectations |
| Scroll Depth (average) | > 60% | < 30% content not being consumed |
| Excessive Scroll Rate | < 5% | > 10% information architecture issues |

**Diagnostic points**:
- Rage clicks concentrated on a specific page → that page has severe interaction issues
- High dead clicks → users think they can click but can't (visual misleading)
- High quick backs → landing page content doesn't match search intent
- Low scroll depth → poor content quality or insufficient above-the-fold info to retain users
- Compare by device dimension → discover mobile-specific UX issues

**Correlation with GA4 metrics**:
| Clarity Signal | GA4 Validation | Combined Assessment |
|---------------|----------------|-------------------|
| High rage clicks | High bounce rate | Confirms UX causes users to leave |
| High dead clicks | Low engagement rate | Users attempt interaction but fail |
| High quick backs | Low session duration | Content doesn't match search intent |
| High scroll depth | But low conversion | Content engages but CTA ineffective |

---

## Six Analysis Dimensions

### 1. SEO

**Primary data source**: GSC Search Analytics

| Metric | Healthy Range | Warning Signal |
|--------|---------------|----------------|
| Average CTR | > 3% (overall) | < 1% requires immediate optimization |
| Average Position | < 20 (first two pages) | > 30 low exposure value |
| Impressions Trend | Steady growth | Sustained decline |
| Index Coverage | > 90% | < 70% structural issues |

**Diagnostic points**:
- High impressions, low CTR → Title/description needs optimization
- Keywords ranked 4-10 → Best optimization targets (push into top 3)
- Pages with declining rankings → Content needs updating or competitors overtaking

### 2. Performance

**Primary data source**: PageSpeed Insights API + agent-browser profiling

| Metric | Good | Needs Improvement | Poor |
|--------|------|-------------------|------|
| LCP (Largest Contentful Paint) | < 2.5s | 2.5-4s | > 4s |
| INP (Interaction to Next Paint) | < 200ms | 200-500ms | > 500ms |
| CLS (Cumulative Layout Shift) | < 0.1 | 0.1-0.25 | > 0.25 |
| TTFB (Time to First Byte) | < 800ms | 800-1800ms | > 1800ms |

### 3. Content Strategy

**Primary data source**: GA4 top_pages + GSC search_analytics

**Diagnostic points**:
- **High-traffic low-engagement pages**: High pageViews but low engagementRate → Content quality doesn't match user expectations
- **High-ranking low-traffic pages**: Good rankings but low clicks → Title/description lacks appeal
- **Zero-traffic content**: Indexed but no impressions → Keyword strategy failure or poor content quality
- **Content decay**: Pages with sustained traffic decline → Needs updating or merging

### 4. User Experience (UX)

**Primary data source**: GA4 user_behavior + landing_pages

| Metric | Healthy Range | Warning Signal |
|--------|---------------|----------------|
| Bounce Rate | < 50% | > 70% (non-blog sites) |
| Engagement Rate | > 60% | < 40% |
| Average Session Duration | > 2 min | < 30s |
| Page Depth | > 2 | = 1 (single-page exit) |

**Diagnostic points**:
- Mobile bounce rate much higher than desktop → Poor mobile experience
- Specific pages with abnormally high bounce rate → Page content or design issues
- Very short session duration → Slow page load or irrelevant content

### 5. Conversion Rate Optimization

**Primary data source**: GA4 conversion_events + landing_pages

**Diagnostic points**:
- Large conversion rate variance across landing pages → A/B testing opportunity
- High-traffic low-conversion pages → CTA or user path issues
- Conversion funnel drop-off points → Identify where users are lost
- Cross-device conversion rate differences → Device-specific experience issues

### 6. Technical Issues

**Primary data source**: GSC URL Inspect + source code analysis + agent-browser

**Checklist**:
- [ ] robots.txt configured correctly
- [ ] sitemap.xml complete and accessible
- [ ] No 4xx/5xx error pages
- [ ] Pages have correct meta tags
- [ ] Structured data (JSON-LD) error-free
- [ ] Mobile-friendly (viewport meta)
- [ ] HTTPS configured correctly
- [ ] No mixed content warnings
- [ ] Images have alt attributes
- [ ] No broken internal links

## Bing Webmaster Metrics

> **When to use**: When `BING_WEBMASTER_API_KEY` is configured. Bing data is analyzed alongside GSC in Phase 2.

**Primary data source**: Bing Webmaster API (`bing_query.py`)

**Key data retention note**: Bing only retains **6 months** of data (vs GSC's ~16 months). Set up regular data collection to avoid gaps.

### Traffic Metrics

| Metric | Healthy Range | Warning Signal |
|--------|---------------|----------------|
| Average CTR (Bing) | > 2% (overall) | < 0.5% requires optimization |
| Average Position (Bing) | < 20 | > 30 low exposure value |
| Impressions Trend | Steady growth or stable | Sustained decline |
| Crawl Success Rate | > 95% | < 85% crawl issues exist |

### Diagnostic Points

- **High impressions, low CTR on Bing** → Title/description may not match Bing users' intent; Bing users skew older and may prefer different phrasing
- **Keywords ranking well on Google but poorly on Bing** → Content authority signals differ; check backlink profile via `links` mode
- **Keywords ranking well on Bing but poorly on Google** → Potential quick-win opportunity to improve Google rankings for these terms
- **Crawl errors** → Check `crawl_stats` mode; Bing crawl issues can suppress rankings independently of Google
- **Low Bing impressions vs Google** → Site may not be fully indexed on Bing; submit sitemap via Bing Webmaster Tools

### Google vs Bing Cross-Engine Comparison

| Dimension | Interpretation |
|-----------|---------------|
| Same top queries on both | Strong brand/content authority; keyword strategy validated |
| Different top queries | User intent differs by engine; optimize content for each |
| Much higher CTR on Bing | Titles/descriptions resonate better with Bing audience; apply learnings to GSC pages |
| Much higher CTR on Google | Meta descriptions may need tuning for Bing; check if rich snippets display differently |
| Pages ranking on Bing but not Google | Check GSC index coverage; may need internal linking improvements |

### Bing-Exclusive Capabilities

| Feature | Mode | Usage |
|---------|------|-------|
| Keyword research & volume | `keyword`, `related_keywords` | Find new keyword opportunities unavailable in GSC |
| Backlink analysis | `links` | Identify high-value inbound links and gaps |
| Crawl health | `crawl_stats` | Diagnose Bing-specific crawl issues |
| Keyword + page detail | `query_page_detail` | Pinpoint exact query-page performance |

## Priority Matrix

Classified by **Impact** x **Implementation Effort**:

| Priority | Impact | Effort | Typical Items |
|----------|--------|--------|---------------|
| P0 Critical | High | Low | Fix 4xx errors, add meta descriptions, fix indexing issues |
| P1 High | High | Medium | Optimize high-impression low-CTR pages, improve Core Web Vitals |
| P2 Medium | Medium | Medium | Content updates, landing page optimization, add structured data |
| P3 Low | Low/Medium | High | Large-scale refactoring, internationalization, new feature development |
