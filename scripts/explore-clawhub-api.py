#!/usr/bin/env python3
"""
Explore ClawHub API
Try to discover and test ClawHub API endpoints
"""

import requests
import json
from typing import Dict, List, Optional

CLAWHUB_BASE = "https://clawhub.ai"
CONVEX_SITE = "https://clawhub.convex.site"  # Common Convex deployment pattern

# Common API patterns to try
ENDPOINTS_TO_TRY = [
    "/api/skills",
    "/api/skills/search",
    "/api/skills/list",
    "/api/v1/skills",
    "/api/v1/skills/search",
    "/_convex/api/skills",
    "/_convex/http/skills",
]

def try_endpoint(base_url: str, endpoint: str, method: str = "GET", params: Optional[Dict] = None) -> Optional[Dict]:
    """Try an API endpoint"""
    url = f"{base_url}{endpoint}"

    print(f"\n🔍 Trying: {method} {url}")
    if params:
        print(f"   Params: {params}")

    try:
        if method == "GET":
            response = requests.get(url, params=params, timeout=5)
        elif method == "POST":
            response = requests.post(url, json=params, timeout=5)
        else:
            return None

        print(f"   Status: {response.status_code}")

        if response.status_code == 200:
            try:
                data = response.json()
                print(f"   ✅ Success! Response:")
                print(f"      {json.dumps(data, indent=2)[:500]}")
                return data
            except:
                print(f"   Response (not JSON): {response.text[:200]}")
        elif response.status_code == 404:
            print(f"   ❌ Not found")
        else:
            print(f"   Response: {response.text[:200]}")

        return None
    except requests.RequestException as e:
        print(f"   ❌ Error: {e}")
        return None


def main():
    """Explore ClawHub API"""

    print("=" * 70)
    print("🕵️  ClawHub API Explorer")
    print("=" * 70)

    print("\n📌 Known URLs:")
    print(f"   Web: {CLAWHUB_BASE}")
    print(f"   Convex: {CONVEX_SITE}")

    print("\n" + "=" * 70)
    print("🔍 Testing ClawHub main site...")
    print("=" * 70)

    for endpoint in ENDPOINTS_TO_TRY:
        try_endpoint(CLAWHUB_BASE, endpoint)

    print("\n" + "=" * 70)
    print("🔍 Testing Convex deployment...")
    print("=" * 70)

    for endpoint in ENDPOINTS_TO_TRY:
        try_endpoint(CONVEX_SITE, endpoint)

    print("\n" + "=" * 70)
    print("🔍 Testing search functionality...")
    print("=" * 70)

    search_queries = [
        {"q": "pdf"},
        {"query": "pdf"},
        {"search": "pdf"},
        {"term": "pdf"},
    ]

    for params in search_queries:
        try_endpoint(CLAWHUB_BASE, "/api/skills/search", params=params)
        try_endpoint(CONVEX_SITE, "/api/skills/search", params=params)

    print("\n" + "=" * 70)
    print("📝 Summary")
    print("=" * 70)
    print("\nTo fully understand ClawHub API, we need to:")
    print("1. Check the ClawHub GitHub repo for API documentation")
    print("2. Look at the clawhub CLI source code to see how it calls the API")
    print("3. Use browser DevTools to inspect network requests on clawhub.ai")
    print("\nNext steps:")
    print("   git clone https://github.com/clawdbot/clawhub")
    print("   cd clawhub")
    print("   cat packages/schema/src/index.ts")
    print("   cat convex/http.ts")


if __name__ == "__main__":
    main()
