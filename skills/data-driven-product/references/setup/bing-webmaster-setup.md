# Bing Webmaster Tools Configuration Guide

## Overview

Bing Webmaster provides Bing search performance data, keyword research (not available in GSC), backlink analysis, and crawl status. Authentication is via API Key.

## Configuration Steps

### 1. Get API Key

1. Open [Bing Webmaster Tools](https://www.bing.com/webmasters/) and sign in
2. If your site isn't added yet, add it and complete verification
3. Click the gear icon (Settings) in the top right → "API Access"
4. Accept terms → Click "Generate API Key" → Copy

> Each account can only have one API Key. If compromised, delete and regenerate.

### 2. Write to .env

```bash
BING_WEBMASTER_API_KEY=your_api_key_here
```

The site URL uses the shared `SITE_URL` — no separate configuration needed.

## Important Limitations

| Item | Description |
|------|-------------|
| Data retention | **6 months** (GSC retains ~16 months), recommend regular collection |
| Rate limit | ~40-50 requests/day/API Key |
| Authentication | API Key (query parameter) |

## Script Usage

```bash
source "$DATA_DIR/venv/bin/activate"
set -a; source "$DATA_DIR/.env"; set +a

# Top keywords
python scripts/bing_query.py --mode query_stats -o "$DATA_DIR/data/bing_queries.json"

# Top pages
python scripts/bing_query.py --mode page_stats -o "$DATA_DIR/data/bing_pages.json"

# Overall traffic trends
python scripts/bing_query.py --mode rank_traffic -o "$DATA_DIR/data/bing_traffic.json"

# Backlinks
python scripts/bing_query.py --mode links -o "$DATA_DIR/data/bing_links.json"

# Crawl status
python scripts/bing_query.py --mode crawl_stats -o "$DATA_DIR/data/bing_crawl.json"

# Keyword research (capability not available in GSC)
python scripts/bing_query.py --mode keyword --query "image compressor" --country us
python scripts/bing_query.py --mode related_keywords --query "image compressor" --country us
```

### Available Modes

| Mode | Description |
|------|-------------|
| `query_stats` | Top keywords + impressions/clicks/rankings |
| `page_stats` | Top pages + traffic data |
| `rank_traffic` | Daily impressions/clicks overview |
| `query_detail` | Detailed data for a specific keyword |
| `page_detail` | All driving keywords for a specific page |
| `query_page_detail` | Specific keyword + page combination |
| `keyword` | Keyword search volume (exclusive capability) |
| `related_keywords` | Related keyword suggestions (exclusive capability) |
| `links` | Backlink analysis (exclusive capability) |
| `crawl_stats` | Crawl frequency and errors |

### Bing-Exclusive Capabilities (Not Available in GSC)

- **Keyword research**: `keyword` and `related_keywords` modes provide search volume data
- **Backlink analysis**: `links` mode provides inbound pages and link counts
- **Crawl health**: `crawl_stats` provides detailed crawl diagnostics
