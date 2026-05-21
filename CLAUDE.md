# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Overview

This is a Claude Code skill that performs goal-driven website analysis using Google Search Console (GSC), GA4, and Bing Webmaster APIs. It collects data, audits sites for SEO/GEO readiness, and generates prioritized improvement reports with charts.

Core principle: **Goal → Data → Gap → Action** — every analysis starts from the website's intended user journey and finds where reality diverges.

## Project Structure

- `skills/data-driven-product/SKILL.md` — The main skill definition (workflow phases, instructions)
- `skills/data-driven-product/scripts/` — Python data collection scripts (GA4, GSC, Bing, PSI, SEO/GEO audit)
- `skills/data-driven-product/references/` — Reference docs (metrics glossary, report template, visualization guide, checklist)
- `.skills-data/data-driven-product/` — Runtime data directory (created per-project when skill runs)

## Python Environment

Uses `uv` with Python 3.12. Dependencies in `skills/data-driven-product/scripts/pyproject.toml`.

```bash
# Setup (once per project)
DATA_DIR=".skills-data/data-driven-product"
uv venv "$DATA_DIR/venv" --python 3.12
uv pip install -p "$DATA_DIR/venv" -r skills/data-driven-product/scripts/pyproject.toml

# Running scripts (always activate venv first)
source "$DATA_DIR/venv/bin/activate"
python skills/data-driven-product/scripts/ga4_query.py
```

## Key Design Decisions

- **All data analysis must be done through code execution** — never manually read JSON and summarize. Write scripts in `$DATA_DIR/scripts/` that read from `$DATA_DIR/data/` and output to `$DATA_DIR/analysis/`.
- **Every analysis phase must generate charts** — saved as PNG to `$DATA_DIR/charts/` and embedded in Markdown reports.
- **Credential auto-discovery** — `utils.py` walks up directories to find `.skills-data/`, loads `.env`, and auto-discovers Service Account JSON from `configs/`.
- **Data directory separation** — `data/` (raw API responses), `analysis/` (processed reports), `charts/` (visualizations), `scripts/` (analysis code).

## Scripts

All scripts import `utils.py` for shared setup (data dir discovery, `.env` loading, Google credential resolution). Key scripts:

| Script | Purpose |
|--------|---------|
| `ga4_query.py` | Collect GA4 traffic/behavior/conversion data |
| `gsc_query.py` | Collect GSC search performance data |
| `bing_query.py` | Collect Bing Webmaster data |
| `ga4_funnel.py` | Funnel exploration (v1alpha API) |
| `perf_audit.py` | PageSpeed Insights collection |
| `seo_audit.py` | SEO metadata audit |
| `geo_audit.py` | GEO/AI-search readiness audit |

## Installation

```bash
npx skills add morvanzhou/data-driven-product
```
