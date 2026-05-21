# HTML Report Template

The deliverable is a self-contained HTML file rendered with ECharts interactive charts. The report generation script reads `$DATA_DIR/analysis/*.json` and assembles the complete HTML.

---

## Report Structure

```
1. Executive Summary
   - Site info + analysis period
   - Core metric cards (3-5 most important numbers)
   - One-sentence conclusion

2. Analysis Sections (dynamically generated based on module combination)
   - One card per module
   - Each card contains: title, key findings, charts, recommendations table

3. Action Items
   - Grouped by priority P0-P3
   - Each recommendation includes: issue, data evidence, recommended action, expected benefit

4. Data Gap Notes (optional)
   - Which analyses couldn't be completed due to missing data
   - How to obtain the missing data
```

## Complete HTML Template

```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Product Data Analysis Report - {{site_name}}</title>
    <script src="https://cdn.jsdelivr.net/npm/echarts@5/dist/echarts.min.js"></script>
    <style>
        :root {
            --color-primary: #4285F4;
            --color-danger: #EA4335;
            --color-warning: #FBBC04;
            --color-success: #34A853;
            --color-bg: #f5f7fa;
            --color-card: #ffffff;
            --color-text: #1a1a2e;
            --color-text-secondary: #4a4a6a;
            --color-border: #e8eaf0;
        }
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body {
            font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
            background: var(--color-bg);
            color: var(--color-text);
            line-height: 1.6;
            padding: 24px;
        }
        .container { max-width: 1200px; margin: 0 auto; }

        /* Header */
        .header {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            border-radius: 16px;
            padding: 40px;
            color: white;
            margin-bottom: 24px;
        }
        .header h1 { font-size: 28px; margin-bottom: 8px; }
        .header .subtitle { opacity: 0.9; font-size: 15px; }
        .header .meta { margin-top: 16px; font-size: 13px; opacity: 0.8; }

        /* Metric Cards */
        .metrics-row {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 16px;
            margin-bottom: 24px;
        }
        .metric-card {
            background: var(--color-card);
            border-radius: 12px;
            padding: 20px;
            text-align: center;
            box-shadow: 0 2px 8px rgba(0,0,0,0.04);
        }
        .metric-card .value { font-size: 32px; font-weight: 700; color: var(--color-primary); }
        .metric-card .label { font-size: 13px; color: var(--color-text-secondary); margin-top: 4px; }
        .metric-card .trend { font-size: 12px; margin-top: 6px; }
        .metric-card .trend.up { color: var(--color-success); }
        .metric-card .trend.down { color: var(--color-danger); }

        /* Section Cards */
        .card {
            background: var(--color-card);
            border-radius: 12px;
            padding: 28px;
            margin-bottom: 24px;
            box-shadow: 0 2px 8px rgba(0,0,0,0.04);
        }
        .card h2 { font-size: 18px; margin-bottom: 16px; padding-bottom: 12px; border-bottom: 1px solid var(--color-border); }
        .card h3 { font-size: 15px; margin: 16px 0 8px; color: var(--color-text-secondary); }
        .card p { margin-bottom: 12px; font-size: 14px; }

        /* Charts */
        .chart-box { width: 100%; height: 400px; margin: 16px 0; }
        .chart-box.small { height: 280px; }
        .chart-box.large { height: 500px; }
        .chart-grid { display: grid; grid-template-columns: 1fr 1fr; gap: 16px; }

        /* Tables */
        table { width: 100%; border-collapse: collapse; font-size: 14px; margin: 12px 0; }
        th, td { padding: 10px 12px; text-align: left; border-bottom: 1px solid var(--color-border); }
        th { background: var(--color-bg); font-weight: 600; font-size: 13px; }

        /* Tags */
        .tag { display: inline-block; padding: 3px 10px; border-radius: 4px; font-size: 12px; font-weight: 500; }
        .tag-p0 { background: #fde8e8; color: #c0392b; }
        .tag-p1 { background: #fef3cd; color: #d68910; }
        .tag-p2 { background: #d4edda; color: #1e7e34; }
        .tag-p3 { background: #e8eaf6; color: #5c6bc0; }
        .tag-growth { background: #d4edda; color: #1e7e34; }
        .tag-plateau { background: #fef3cd; color: #d68910; }
        .tag-decline { background: #fde8e8; color: #c0392b; }

        /* Recommendations */
        .recommendation {
            border-left: 4px solid var(--color-primary);
            padding: 12px 16px;
            margin: 12px 0;
            background: #f8f9fc;
            border-radius: 0 8px 8px 0;
        }
        .recommendation.p0 { border-left-color: var(--color-danger); }
        .recommendation.p1 { border-left-color: #FF6D01; }
        .recommendation.p2 { border-left-color: var(--color-warning); }
        .recommendation.p3 { border-left-color: var(--color-success); }
        .recommendation .title { font-weight: 600; margin-bottom: 4px; }
        .recommendation .evidence { font-size: 13px; color: var(--color-text-secondary); }

        /* Responsive */
        @media (max-width: 768px) {
            .chart-grid { grid-template-columns: 1fr; }
            .header { padding: 24px; }
            .header h1 { font-size: 22px; }
            body { padding: 12px; }
        }
    </style>
</head>
<body>
<div class="container">

    <!-- ═══ HEADER ═══ -->
    <div class="header">
        <h1>Product Data Analysis Report</h1>
        <div class="subtitle">{{site_url}} — {{analysis_type_description}}</div>
        <div class="meta">Analysis period: {{date_range}} | Generated: {{generated_at}} | Data sources: {{data_sources}}</div>
    </div>

    <!-- ═══ EXECUTIVE SUMMARY METRICS ═══ -->
    <div class="metrics-row">
        <!-- Dynamically generated metric cards -->
    </div>

    <!-- ═══ ANALYSIS SECTIONS ═══ -->
    <!-- One card per analysis module, dynamically generated -->

    <!-- ═══ ACTION ITEMS ═══ -->
    <div class="card">
        <h2>Action Items</h2>
        <!-- Recommendations grouped by P0-P3 -->
    </div>

</div>

<script>
// ═══ CHART DATA & INITIALIZATION ═══
const chartConfigs = {{charts_json}};

// Initialize all charts
document.addEventListener('DOMContentLoaded', function() {
    chartConfigs.forEach(function(config) {
        const dom = document.getElementById(config.id);
        if (dom) {
            const chart = echarts.init(dom);
            chart.setOption(config.option);
            // Responsive
            window.addEventListener('resize', function() { chart.resize(); });
        }
    });
});
</script>
</body>
</html>
```

## Template Variable Reference

| Variable | Source | Description |
|----------|--------|-------------|
| `{{site_name}}` | website-profile.json | Site name |
| `{{site_url}}` | .env SITE_URL | Site URL |
| `{{analysis_type_description}}` | Selected analysis modules | e.g., "Pre-Analysis + Post-Analysis" |
| `{{date_range}}` | Data collection parameters | e.g., "2025-04-01 ~ 2025-04-28" |
| `{{generated_at}}` | Generation time | ISO format |
| `{{data_sources}}` | Actually configured data sources | e.g., "GA4 + GSC + Clarity" |
| `{{charts_json}}` | Aggregated chart configurations | JSON array, each item contains id + option |

## Report Content Organization Principles

1. **Order by decision value**: Most important findings and recommendations first
2. **Data → Insight → Action**: Each module shows data charts first, then interpretation, then action recommendations
3. **Priority labels**: All recommendations must be labeled P0-P3 priority
4. **Quantified benefit estimates**: Provide expected post-optimization benefit numbers whenever possible

Save report to `$DATA_DIR/reports/report.html`.
