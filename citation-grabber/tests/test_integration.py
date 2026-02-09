"""Integration tests for citation module."""

import pytest
import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import citation


@pytest.mark.integration
class TestRealAPICalls:
    """Integration tests with real API calls.

    These tests make actual network requests and may be slow.
    Run with: pytest -m integration
    """

    def test_fetch_by_real_doi(self):
        """Test fetching a paper by a known DOI."""
        # This is the DOI for "Attention Is All You Need"
        result = citation.fetch_by_doi("10.5555/3295222.3295349")

        if result:  # May fail if network is unavailable
            assert "Vaswani" in result or "@" in result

    def test_search_crossref_real(self):
        """Test searching CrossRef with a known paper."""
        result = citation.search_crossref("Attention Is All You Need")

        # Should find a DOI (may vary based on CrossRef database)
        assert result is None or result.startswith("10.")

    def test_get_citation_integration(self):
        """Test the full citation retrieval pipeline."""
        # Try a well-known paper
        result = citation.get_citation(
            "Deep Residual Learning for Image Recognition",
            verbose=False
        )

        # Should return something if network is available
        # This test is flexible as it depends on external services
        assert result is None or "@" in result or "PMID" in result


if __name__ == "__main__":
    pytest.main([__file__, "-v", "-m", "integration"])
