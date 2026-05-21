# Microsoft Clarity Configuration Guide

## Overview

Microsoft Clarity provides user behavior quality data: heatmap metrics, rage clicks, dead clicks, scroll depth, and quick backs. Access is via Bearer Token authentication through the Data Export API.

## Configuration Steps

### 1. Ensure Clarity is Installed on Your Website

1. Open [Microsoft Clarity](https://clarity.microsoft.com/)
2. If no project exists, click "Add new project" → Enter website URL
3. Install the Clarity tracking code on your website (or via Google Tag Manager)

### 2. Generate API Token

1. In your Clarity project, click **Settings** (left menu)
2. Find the **"Data Export"** section
3. Click **"Generate API token"**
4. Copy the generated token

> Only project administrators (Admin) can generate tokens. Token format: 4-32 alphanumeric characters, hyphens, underscores, and periods.

### 3. Write to .env

```bash
CLARITY_API_TOKEN=your_token_here
CLARITY_PROJECT_ID=your_project_id   # Get from Clarity URL (e.g., clarity.microsoft.com/projects/view/XXXXXX)
```

## Important Limitations

| Item | Description |
|------|-------------|
| Data window | Only the last **1-3 days** (not historical data) |
| Rate limit | **10 requests/project/day** |
| Available data | Aggregated metrics (not individual sessions) |
| Not available | Heatmap images, session replay recordings (UI only) |

## API Returned Metrics

| Metric | Description | Analysis Use |
|--------|-------------|-------------|
| `TrafficCount` | Traffic count | Baseline comparison |
| `ScrollDepth` | Average scroll depth | Content consumption level |
| `DeadClickCount` | Dead click count | UI clickability issues |
| `RageClickCount` | Rage click count | User frustration |
| `QuickBackCount` | Quick back count | Landing page doesn't meet expectations |
| `ExcessiveScrollCount` | Excessive scroll count | Information architecture issues |
| `EngagementTime` | Engagement time | True engagement level |

## Available Dimensions (API breakdown)

| Dimension Parameter | Description |
|--------------------|-------------|
| `OS` | Operating system |
| `Browser` | Browser |
| `Country` | Country |
| `Device` | Device type |
| `Source` | Traffic source |
| `Channel` | Traffic channel |
| `URL` | Page URL |

## Script Usage

```bash
source "$DATA_DIR/venv/bin/activate"
set -a; source "$DATA_DIR/.env"; set +a

# Overall overview (last 3 days)
python scripts/clarity_query.py --days 3 -o "$DATA_DIR/data/clarity_overview.json"

# By device breakdown
python scripts/clarity_query.py --days 3 --dimension Device -o "$DATA_DIR/data/clarity_device.json"

# By page URL breakdown
python scripts/clarity_query.py --days 3 --dimension URL -o "$DATA_DIR/data/clarity_urls.json"

# By country breakdown
python scripts/clarity_query.py --days 3 --dimension Country -o "$DATA_DIR/data/clarity_country.json"

# By source breakdown
python scripts/clarity_query.py --days 3 --dimension Source -o "$DATA_DIR/data/clarity_source.json"

# Multi-dimension (up to 3)
python scripts/clarity_query.py --days 3 --dimension Device --dimension2 Country -o "$DATA_DIR/data/clarity_device_country.json"
```

## Complementary Relationship with Other Tools

| Capability | GA4 | Clarity |
|-----------|-----|---------|
| Traffic statistics | ✅ Complete | ⚠️ Only 1-3 days |
| User paths | ✅ Page-level | ❌ API not supported |
| Conversion funnels | ✅ Event-level | ❌ API not supported |
| UX quality signals | ❌ | ✅ rage/dead clicks |
| Scroll depth | ❌ | ✅ |
| Quick back detection | ❌ | ✅ |
| Heatmaps | ❌ | ⚠️ UI only |

**Best practice**: Use GA4 for traffic and conversion analysis, use Clarity for UX quality diagnosis. Combined, they answer "users arrive but why don't they convert."
