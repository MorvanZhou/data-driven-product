#!/usr/bin/env python3
"""Microsoft Clarity Data Export API query tool.

Usage:
    python clarity_query.py --days 3 -o clarity_overview.json
    python clarity_query.py --days 3 --dimension Device -o clarity_device.json
    python clarity_query.py --days 3 --dimension URL --dimension2 Country

Reads .env from: .skills-data/data-driven-product/.env
Env vars: CLARITY_API_TOKEN
"""

import argparse
import json
import os
import sys

import utils  # noqa: F401 — triggers .env loading & warning suppression
import requests


API_BASE = "https://www.clarity.ms/export-data/api/v1"

VALID_DIMENSIONS = ["OS", "Browser", "Country", "Device", "Source", "Channel", "URL"]


def get_token():
    token = os.environ.get("CLARITY_API_TOKEN")
    if not token:
        print("Error: CLARITY_API_TOKEN not set in .env", file=sys.stderr)
        sys.exit(1)
    return token


def query_live_insights(token, num_days, dimensions=None):
    """Query Clarity Data Export API for project live insights."""
    url = f"{API_BASE}/project-live-insights"
    params = {"numOfDays": num_days}

    if dimensions:
        for i, dim in enumerate(dimensions[:3], 1):
            params[f"dimension{i}"] = dim

    headers = {"Authorization": f"Bearer {token}"}
    response = requests.get(url, params=params, headers=headers, timeout=30)

    if response.status_code == 401:
        print("Error: Invalid or expired CLARITY_API_TOKEN", file=sys.stderr)
        sys.exit(1)
    elif response.status_code == 429:
        print("Error: Rate limit exceeded (max 10 requests/project/day)", file=sys.stderr)
        sys.exit(1)
    elif response.status_code != 200:
        print(f"Error: HTTP {response.status_code} — {response.text}", file=sys.stderr)
        sys.exit(1)

    return response.json()


def main():
    parser = argparse.ArgumentParser(description="Microsoft Clarity Data Export API query tool")
    parser.add_argument("--days", type=int, choices=[1, 2, 3], default=3,
                        help="Number of days to look back (1-3, default: 3)")
    parser.add_argument("--dimension", choices=VALID_DIMENSIONS,
                        help="Primary breakdown dimension")
    parser.add_argument("--dimension2", choices=VALID_DIMENSIONS,
                        help="Secondary breakdown dimension")
    parser.add_argument("--dimension3", choices=VALID_DIMENSIONS,
                        help="Tertiary breakdown dimension")
    parser.add_argument("--output", "-o", help="Output file path (default: stdout)")

    args = parser.parse_args()

    token = get_token()

    dimensions = []
    if args.dimension:
        dimensions.append(args.dimension)
    if args.dimension2:
        dimensions.append(args.dimension2)
    if args.dimension3:
        dimensions.append(args.dimension3)

    data = query_live_insights(token, args.days, dimensions or None)

    result = {
        "source": "microsoft_clarity",
        "num_days": args.days,
        "dimensions": dimensions or [],
        "data": data,
    }

    output = json.dumps(result, indent=2, ensure_ascii=False)
    if args.output:
        os.makedirs(os.path.dirname(os.path.abspath(args.output)), exist_ok=True)
        with open(args.output, "w", encoding="utf-8") as f:
            f.write(output)
        print(f"Output written to {args.output}", file=sys.stderr)
    else:
        print(output)


if __name__ == "__main__":
    main()
