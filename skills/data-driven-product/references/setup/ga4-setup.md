# Google Analytics 4 (GA4) Configuration Guide

## Overview

GA4 provides user behavior data: traffic, page views, conversion events, user profiles, and funnels. Access is via Service Account authentication.

GA4 shares the same Google Service Account as GSC. If GSC is already configured, you only need to additionally authorize GA4 access.

## Configuration Steps

### 1. Enable Analytics Data API

If you don't yet have a Google Cloud project, first follow steps 1-2 in the [GSC Configuration Guide](gsc-setup.md).

1. Open [API Library](https://console.cloud.google.com/apis/library)
2. Search for **"Google Analytics Data API"** → Click "Enable"

### 2. Authorize Service Account in GA4

1. Open [Google Analytics](https://analytics.google.com/)
2. Click the gear icon (Admin) in the bottom left
3. Under "Property", click "Property Access Management"
4. Click "+" (top right) → "Add users"
5. Paste Service Account email → Role: "Viewer" → "Add"

### 3. Get GA4 Property ID

1. On the Analytics Admin page, under "Property", click "Property Settings"
2. The numeric string shown in the top right is the Property ID (e.g., `123456789`, without "UA-" prefix)

### 4. Write to .env

```bash
GA4_PROPERTY_ID=123456789
```

## Script Usage

### Preset Query Templates

```bash
source "$DATA_DIR/venv/bin/activate"
set -a; source "$DATA_DIR/.env"; set +a

python scripts/ga4_query.py --preset traffic_overview -o "$DATA_DIR/data/ga4_traffic.json"
python scripts/ga4_query.py --preset top_pages --limit 100 -o "$DATA_DIR/data/ga4_pages.json"
python scripts/ga4_query.py --preset user_acquisition -o "$DATA_DIR/data/ga4_acquisition.json"
python scripts/ga4_query.py --preset device_breakdown -o "$DATA_DIR/data/ga4_devices.json"
python scripts/ga4_query.py --preset landing_pages --limit 50 -o "$DATA_DIR/data/ga4_landing.json"
python scripts/ga4_query.py --preset user_behavior --limit 100 -o "$DATA_DIR/data/ga4_behavior.json"
python scripts/ga4_query.py --preset conversion_events -o "$DATA_DIR/data/ga4_conversions.json"
```

### Available Presets

| Preset | Purpose |
|--------|---------|
| `traffic_overview` | Daily traffic trends |
| `top_pages` | Top pages |
| `user_acquisition` | User acquisition channels |
| `device_breakdown` | Device distribution |
| `geo_distribution` | Geographic distribution |
| `landing_pages` | Landing page performance |
| `user_behavior` | User behavior |
| `conversion_events` | Conversion events |
| `demographics_age` | Age distribution (requires Google Signals) |
| `demographics_gender` | Gender distribution (requires Google Signals) |
| `demographics_geo` | Country + city distribution |
| `demographics_language` | Language distribution |
| `demographics_interests` | Interest categories (requires Google Signals) |
| `new_vs_returning` | New vs returning users |

### Custom Queries

```bash
python scripts/ga4_query.py \
    --dimensions pagePath,deviceCategory \
    --metrics sessions,bounceRate,averageSessionDuration \
    --start-date 2025-01-01 --end-date 2025-03-01 \
    --order-by="-sessions" --limit 200
```

### Date Formats

Supports absolute dates (`2025-01-01`) and relative dates (`today`, `yesterday`, `NdaysAgo`).

### Funnel Analysis (ga4_funnel.py)

```bash
# Simple funnel
python scripts/ga4_funnel.py --steps "page_view,signup,purchase" -o "$DATA_DIR/data/ga4_funnel.json"

# With dimension breakdown
python scripts/ga4_funnel.py --steps "page_view,add_to_cart,purchase" --breakdown deviceCategory

# Trended funnel
python scripts/ga4_funnel.py --steps "page_view,purchase" --trended --start-date 30daysAgo
```

Advanced funnel configuration supports JSON config files with field_filter, within_duration, directly_followed_by, and more.

> **Note**: `ga4_funnel.py` uses the GA4 v1alpha API (functional but may have breaking changes).
