# Google Search Console (GSC) Configuration Guide

## Overview

GSC provides search performance data: keyword rankings, click-through rates, impressions, and index status. Access is via Service Account authentication.

## Configuration Steps

### 1. Create a Google Cloud Project and Enable API

1. Open [Google Cloud Console](https://console.cloud.google.com/)
2. Project selector → "New Project" → Name it (e.g., "my-site-analytics") → "Create"
3. Confirm you've switched to the new project, open [API Library](https://console.cloud.google.com/apis/library)
4. Search for **"Google Search Console API"** → Click "Enable"
5. Search for **"PageSpeed Insights API"** → Click "Enable" (for performance audits)

### 2. Create a Service Account and Download JSON Key

1. Open [Service Accounts page](https://console.cloud.google.com/iam-admin/serviceaccounts)
2. Click "+ Create Service Account"
3. Enter a name (e.g., "analytics-reader") → "Create and Continue"
4. Skip role selection → "Continue" → "Done"
5. Click the Service Account email to enter the details page
6. "Keys" tab → "Add Key" → "Create new key" → Select **JSON** → "Create"
7. Browser automatically downloads the `.json` file
8. Note the Service Account email address (format: `analytics-reader@project.iam.gserviceaccount.com`)

### 3. Place the JSON Key

```bash
cp /path/to/downloaded/key.json "$DATA_DIR/configs/"
```

Scripts auto-discover `*.json` key files from `$DATA_DIR/configs/` via `utils.py`.

### 4. Authorize in Search Console

1. Open [Google Search Console](https://search.google.com/search-console/)
2. Select your website property
3. "Settings" → "Users and permissions"
4. "Add user" → Paste Service Account email → Permission: "Restricted" (read-only) → "Add"

### 5. Confirm GSC Property Type

GSC has two property types; `GSC_SITE_URL` must match the actual type:

| Property Type | GSC_SITE_URL Format | Example |
|--------------|--------------------:|---------|
| **Domain property** | `sc-domain:domain` | `sc-domain:example.com` |
| **URL-prefix property** | Full URL | `https://example.com` |

> In the Search Console property selector, if it shows a bare domain it's a Domain property (use the `sc-domain:` prefix); if it shows a full URL it's a URL-prefix property. Using the wrong format will result in a 403 error.

### 6. Write to .env

```bash
GSC_SITE_URL=sc-domain:example.com   # or https://example.com
```

## Script Usage

```bash
source "$DATA_DIR/venv/bin/activate"
set -a; source "$DATA_DIR/.env"; set +a

# Keyword data
python scripts/gsc_query.py --dimensions query --limit 500 -o "$DATA_DIR/data/gsc_queries.json"

# Page data
python scripts/gsc_query.py --dimensions page --limit 500 -o "$DATA_DIR/data/gsc_pages.json"

# Device + country
python scripts/gsc_query.py --dimensions device,country -o "$DATA_DIR/data/gsc_devices.json"

# Trends
python scripts/gsc_query.py --dimensions date -o "$DATA_DIR/data/gsc_trends.json"

# Sitemap
python scripts/gsc_query.py --mode sitemaps -o "$DATA_DIR/data/gsc_sitemaps.json"

# URL inspection
python scripts/gsc_query.py --mode inspect --inspect-url "https://example.com/page"
```

### Available Dimensions

| Dimension | Description |
|-----------|-------------|
| `query` | Search query |
| `page` | Page URL |
| `country` | Country code |
| `device` | Device type (DESKTOP/MOBILE/TABLET) |
| `date` | Date |
| `searchAppearance` | Search result appearance type |

### Returned Metrics

Each row contains: `clicks`, `impressions`, `ctr` (click-through rate), `position` (average ranking)

### Custom Queries

```bash
# Specify date range
python scripts/gsc_query.py --dimensions query --limit 500 \
    --start-date 2025-01-01 --end-date 2025-03-01

# Output to file
python scripts/gsc_query.py --dimensions query -o "$DATA_DIR/data/gsc_custom.json"
```

Advanced filtering (e.g., `dimensionFilterGroups`) requires custom scripts; refer to the GSC Search Analytics API documentation.
