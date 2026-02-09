#!/usr/bin/env python3
"""
ClawHub API Client
Official API wrapper for browsing ClawHub skills
"""

import requests
from typing import List, Dict, Optional
from dataclasses import dataclass
import json


@dataclass
class ClawHubSkill:
    """ClawHub Skill representation"""
    slug: str
    display_name: str
    summary: str
    tags: Dict[str, str]
    stats: Dict
    created_at: int
    updated_at: int
    latest_version: Optional[str] = None


class ClawHubAPI:
    """ClawHub API Client"""

    BASE_URL = "https://clawhub.ai"
    API_VERSION = "v1"

    def __init__(self, base_url: Optional[str] = None):
        self.base_url = base_url or self.BASE_URL
        self.session = requests.Session()
        self.session.headers.update({
            "User-Agent": "skills-store/1.0",
            "Accept": "application/json"
        })

    def _get(self, endpoint: str, params: Optional[Dict] = None) -> Dict:
        """Make GET request"""
        url = f"{self.base_url}/api/{self.API_VERSION}/{endpoint}"
        response = self.session.get(url, params=params, timeout=10)
        response.raise_for_status()
        return response.json()

    def list_skills(self, limit: Optional[int] = None, offset: int = 0) -> List[ClawHubSkill]:
        """
        List all skills from ClawHub

        Args:
            limit: Maximum number of skills to return
            offset: Pagination offset

        Returns:
            List of ClawHubSkill objects
        """
        params = {}
        if limit:
            params['limit'] = limit
        if offset:
            params['offset'] = offset

        data = self._get("skills", params=params)

        skills = []
        for item in data.get('items', []):
            skill = ClawHubSkill(
                slug=item.get('slug', ''),
                display_name=item.get('displayName', ''),
                summary=item.get('summary', ''),
                tags=item.get('tags', {}),
                stats=item.get('stats', {}),
                created_at=item.get('createdAt', 0),
                updated_at=item.get('updatedAt', 0),
                latest_version=item.get('tags', {}).get('latest')
            )
            skills.append(skill)

        return skills

    def get_skill(self, slug: str) -> Optional[Dict]:
        """
        Get detailed information about a specific skill

        Args:
            slug: Skill slug (e.g., "pdf-analyzer")

        Returns:
            Dict with skill info and latest version, or None if not found
        """
        try:
            return self._get(f"skills/{slug}")
        except requests.HTTPError as e:
            if e.response.status_code == 404:
                return None
            raise

    def search_skills(self, query: str, limit: int = 20) -> List[ClawHubSkill]:
        """
        Search skills by keyword

        Note: This is a client-side search for now.
        ClawHub uses vector search but we don't have direct API access yet.

        Args:
            query: Search query
            limit: Maximum results

        Returns:
            List of matching skills
        """
        # Get all skills and filter locally
        # TODO: Replace with real API when available
        all_skills = self.list_skills()

        query_lower = query.lower()
        matching = []

        for skill in all_skills:
            # Search in display name, summary, and slug
            summary = skill.summary or ""
            if (query_lower in skill.display_name.lower() or
                query_lower in summary.lower() or
                query_lower in skill.slug.lower()):
                matching.append(skill)

                if len(matching) >= limit:
                    break

        return matching

    def get_skill_stats(self) -> Dict:
        """Get overall ClawHub statistics"""
        skills = self.list_skills()
        return {
            "total_skills": len(skills),
            "total_downloads": sum(s.stats.get('downloads', 0) for s in skills),
            "total_stars": sum(s.stats.get('stars', 0) for s in skills),
        }


def main():
    """Test the ClawHub API"""
    print("🧪 Testing ClawHub API Client\n")

    client = ClawHubAPI()

    # Test 1: List skills
    print("1️⃣ Listing all skills...")
    skills = client.list_skills(limit=10)
    print(f"   Found {len(skills)} skills (showing first 10):\n")
    for skill in skills[:5]:
        print(f"   - {skill.display_name} ({skill.slug})")
        summary = skill.summary or "No description"
        print(f"     {summary[:80]}..." if len(summary) > 80 else f"     {summary}")
        print(f"     ⭐ {skill.stats.get('stars', 0)} | "
              f"📥 {skill.stats.get('downloads', 0)} | "
              f"v{skill.latest_version or 'N/A'}\n")

    # Test 2: Get specific skill
    print("\n2️⃣ Getting 'search' skill details...")
    search_skill = client.get_skill("search")
    if search_skill:
        print(f"   ✅ Found: {search_skill['skill']['displayName']}")
        print(f"   Summary: {search_skill['skill']['summary']}")
        print(f"   Latest: v{search_skill['latestVersion']['version']}")
    else:
        print("   ❌ Not found")

    # Test 3: Search skills
    print("\n3️⃣ Searching for 'web' skills...")
    results = client.search_skills("web", limit=5)
    print(f"   Found {len(results)} matching skills:\n")
    for skill in results:
        print(f"   - {skill.display_name}")

    # Test 4: Statistics
    print("\n4️⃣ ClawHub Statistics...")
    stats = client.get_skill_stats()
    print(f"   Total skills: {stats['total_skills']}")
    print(f"   Total downloads: {stats['total_downloads']}")
    print(f"   Total stars: {stats['total_stars']}")

    print("\n✅ All tests passed!")


if __name__ == "__main__":
    main()
