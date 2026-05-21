"""Check which data sources are configured and report available analysis capabilities.

Usage:
    python check_config.py

Outputs a structured summary to stdout indicating which tools are ready
and what analyses can be performed.
"""

import os
import sys
from pathlib import Path

# Reuse utils for data dir discovery and .env loading
sys.path.insert(0, str(Path(__file__).parent))
from utils import DATA_DIR, find_google_credentials


def main():
    if not DATA_DIR:
        print("ERROR: Cannot locate .skills-data/data-driven-product/ directory.")
        print("Run the skill setup first.")
        sys.exit(1)

    env_path = DATA_DIR / ".env"
    configs_dir = DATA_DIR / "configs"

    # --- Load .env values ---
    env_vars = {}
    if env_path.exists():
        with open(env_path) as f:
            for line in f:
                line = line.strip()
                if not line or line.startswith("#"):
                    continue
                if "=" in line:
                    key, _, val = line.partition("=")
                    env_vars[key.strip()] = val.strip()

    # --- Check each data source ---
    sources = {}

    # Google Service Account (shared by GSC + GA4)
    sa_path = find_google_credentials()
    has_sa = sa_path is not None
    sa_file = Path(sa_path).name if sa_path else None

    # GSC
    gsc_site = env_vars.get("GSC_SITE_URL", "")
    sources["GSC"] = {
        "configured": bool(has_sa and gsc_site),
        "details": {},
        "missing": [],
    }
    if has_sa:
        sources["GSC"]["details"]["service_account"] = sa_file
    else:
        sources["GSC"]["missing"].append("Service Account JSON in configs/")
    if gsc_site:
        sources["GSC"]["details"]["site_url"] = gsc_site
    else:
        sources["GSC"]["missing"].append("GSC_SITE_URL in .env")

    # GA4
    ga4_property = env_vars.get("GA4_PROPERTY_ID", "")
    sources["GA4"] = {
        "configured": bool(has_sa and ga4_property),
        "details": {},
        "missing": [],
    }
    if has_sa:
        sources["GA4"]["details"]["service_account"] = sa_file
    else:
        sources["GA4"]["missing"].append("Service Account JSON in configs/")
    if ga4_property:
        sources["GA4"]["details"]["property_id"] = ga4_property
    else:
        sources["GA4"]["missing"].append("GA4_PROPERTY_ID in .env")

    # Bing Webmaster
    bing_key = env_vars.get("BING_WEBMASTER_API_KEY", "")
    sources["Bing"] = {
        "configured": bool(bing_key),
        "details": {},
        "missing": [],
    }
    if bing_key:
        sources["Bing"]["details"]["api_key"] = bing_key[:6] + "..."
    else:
        sources["Bing"]["missing"].append("BING_WEBMASTER_API_KEY in .env")

    # Microsoft Clarity
    clarity_token = env_vars.get("CLARITY_API_TOKEN", "")
    sources["Clarity"] = {
        "configured": bool(clarity_token),
        "details": {},
        "missing": [],
    }
    if clarity_token:
        sources["Clarity"]["details"]["token"] = clarity_token[:6] + "..."
    else:
        sources["Clarity"]["missing"].append("CLARITY_API_TOKEN in .env")

    # PageSpeed Insights (optional, works without key but rate-limited)
    psi_key = env_vars.get("PSI_API_KEY", "")
    sources["PSI"] = {
        "configured": True,  # Always available, key is optional
        "details": {"api_key": "configured" if psi_key else "not set (rate-limited)"},
        "missing": [],
    }

    # SITE_URL (required for audits)
    site_url = env_vars.get("SITE_URL", "")

    # --- Config files in configs/ ---
    config_files = []
    if configs_dir.is_dir():
        config_files = [f.name for f in sorted(configs_dir.iterdir()) if f.is_file()]

    # === OUTPUT ===
    print("=" * 60)
    print("DATA SOURCE CONFIGURATION STATUS")
    print(f"Data directory: {DATA_DIR}")
    print(f"Site URL: {site_url or '(not set)'}")
    print("=" * 60)
    print()

    # Source status table
    print("┌────────────┬────────────┬─────────────────────────────────┐")
    print("│ Source     │ Status     │ Details                         │")
    print("├────────────┼────────────┼─────────────────────────────────┤")
    for name, info in sources.items():
        status = "✅ Ready" if info["configured"] else "❌ Missing"
        if info["details"]:
            detail = ", ".join(f"{k}={v}" for k, v in info["details"].items())
        elif info["missing"]:
            detail = "Need: " + "; ".join(info["missing"])
        else:
            detail = ""
        print(f"│ {name:<10} │ {status:<10} │ {detail:<31} │")
    print("└────────────┴────────────┴─────────────────────────────────┘")

    if config_files:
        print(f"\nConfig files in configs/: {', '.join(config_files)}")

    # --- Available analyses ---
    print("\n" + "=" * 60)
    print("AVAILABLE ANALYSES")
    print("=" * 60)

    analyses = []

    if sources["GSC"]["configured"]:
        analyses.append(("GSC", "P1", "Keyword Market Demand Analysis (gsc_query.py --dimensions date,query)"))
        analyses.append(("GSC", "P2", "Competitor Traffic Reverse-Engineering (gsc_query.py --dimensions query)"))
        analyses.append(("GSC", "A1", "Page Health - search metrics (gsc_query.py --dimensions page)"))
        analyses.append(("GSC", "A6", "Content Decay Monitoring (gsc_query.py period comparison)"))
        analyses.append(("GSC", "D1", "Lifecycle Assessment - search trends (gsc_query.py --dimensions date)"))

    if sources["GA4"]["configured"]:
        analyses.append(("GA4", "A1", "Page Health - traffic & behavior (ga4_query.py --preset top_pages)"))
        analyses.append(("GA4", "A2", "User Behavior Path Analysis (ga4_query.py --preset user_behavior)"))
        analyses.append(("GA4", "A3", "Conversion Funnel Diagnosis (ga4_funnel.py)"))
        analyses.append(("GA4", "A4", "Traffic Channel ROI (ga4_query.py --preset user_acquisition)"))
        analyses.append(("GA4", "A5", "Device/Geo Differential (ga4_query.py --preset device_breakdown)"))
        analyses.append(("GA4", "A8", "User Persona Analysis (ga4_query.py --preset demographics_*)"))
        analyses.append(("GA4", "D1", "Lifecycle Assessment - traffic trends (ga4_query.py --preset traffic_overview)"))

    if sources["Bing"]["configured"]:
        analyses.append(("Bing", "P1", "Keyword Research & Discovery (bing_query.py --mode keyword)"))
        analyses.append(("Bing", "P2", "Related Keywords for gap analysis (bing_query.py --mode related_keywords)"))

    if sources["Clarity"]["configured"]:
        analyses.append(("Clarity", "A1", "Page UX Quality (clarity_query.py --dimension URL)"))
        analyses.append(("Clarity", "A2", "Rage/Dead Click Analysis (clarity_query.py)"))
        analyses.append(("Clarity", "A4", "Channel UX Quality (clarity_query.py --dimension Channel)"))
        analyses.append(("Clarity", "A5", "Device UX Comparison (clarity_query.py --dimension Device)"))

    if sources["PSI"]["configured"]:
        analyses.append(("PSI", "A7", "Performance & SEO Audit (perf_audit.py)"))

    if site_url:
        analyses.append(("Web", "A7", "SEO Technical Audit (seo_audit.py --url SITE_URL)"))
        analyses.append(("Web", "A7", "GEO/AI-search Readiness (geo_audit.py --url SITE_URL)"))

    if not analyses:
        print("\n⚠️  No data sources configured. Cannot perform any analysis.")
        print("   Configure at least GSC_SITE_URL + Service Account, or BING_WEBMASTER_API_KEY.")
    else:
        print(f"\n{len(analyses)} analyses available:\n")
        for source, module_id, desc in analyses:
            print(f"  [{source:<7}] {module_id}: {desc}")

    # --- Summary for LLM consumption ---
    print("\n" + "=" * 60)
    print("SUMMARY FOR MODEL")
    print("=" * 60)
    ready = [name for name, info in sources.items() if info["configured"]]
    not_ready = [name for name, info in sources.items() if not info["configured"]]
    print(f"Ready: {', '.join(ready) if ready else 'None'}")
    print(f"Not configured: {', '.join(not_ready) if not_ready else 'None'}")
    if ready:
        print(f"\nYou can run analyses using: {', '.join(ready)} data.")
        if "GSC" in ready and "GA4" in ready:
            print("Both GSC + GA4 available → full Post-Analysis (A1-A8) and Decision Analysis (D1-D3) possible.")
        if "Bing" in ready:
            print("Bing available → Pre-Analysis keyword research (P1-P4) possible.")
        if "Clarity" in ready:
            print("Clarity available → UX quality signals for behavior analysis.")


if __name__ == "__main__":
    main()
