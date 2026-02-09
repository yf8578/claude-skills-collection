"""Unit tests for citation module."""

import pytest
from unittest.mock import Mock, patch, mock_open
import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import citation


class TestDetectType:
    """Tests for detect_type function."""

    def test_detect_doi(self):
        assert citation.detect_type("10.1234/example") == "doi"
        assert citation.detect_type("10.5555/3295222.3295349") == "doi"
        assert citation.detect_type("  10.1234/test  ") == "doi"

    def test_detect_pmid(self):
        assert citation.detect_type("12345678") == "pmid"
        assert citation.detect_type("1") == "pmid"
        assert citation.detect_type("  987654321  ") == "pmid"

    def test_detect_title(self):
        assert citation.detect_type("Attention Is All You Need") == "title"
        assert citation.detect_type("Deep Learning Review") == "title"
        assert citation.detect_type("") == "title"


class TestFetchByDOI:
    """Tests for fetch_by_doi function."""

    @patch('citation.requests.get')
    def test_fetch_successful(self, mock_get):
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.text = "@article{test, title={Test}}"
        mock_get.return_value = mock_response

        result = citation.fetch_by_doi("10.1234/example")

        assert result is not None
        assert "@article{test" in result
        assert "10.1234/example" in result

    @patch('citation.requests.get')
    def test_fetch_not_found(self, mock_get):
        mock_response = Mock()
        mock_response.status_code = 404
        mock_get.return_value = mock_response

        result = citation.fetch_by_doi("10.1234/notfound")
        assert result is None

    @patch('citation.requests.get')
    def test_fetch_timeout(self, mock_get):
        mock_get.side_effect = citation.requests.exceptions.Timeout()

        with pytest.raises(citation.APIError):
            citation.fetch_by_doi("10.1234/timeout")


class TestFetchByPMID:
    """Tests for fetch_by_pmid function."""

    @patch('citation.requests.get')
    def test_fetch_bibtex_successful(self, mock_get):
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.text = "@article{pmid123, title={Test}}"
        mock_get.return_value = mock_response

        result = citation.fetch_by_pmid("12345678", "bibtex")

        assert result is not None
        assert "@article{pmid123" in result
        assert "PMID: 12345678" in result

    @patch('citation.requests.get')
    def test_fetch_nbib_successful(self, mock_get):
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.text = "PMID- 12345678\nTI  - Test Title"
        mock_get.return_value = mock_response

        result = citation.fetch_by_pmid("12345678", "nbib")

        assert result is not None
        assert "PMID- 12345678" in result

    @patch('citation.requests.get')
    def test_fetch_not_found(self, mock_get):
        mock_response = Mock()
        mock_response.status_code = 404
        mock_get.return_value = mock_response

        result = citation.fetch_by_pmid("99999999")
        assert result is None


class TestSearchPubMed:
    """Tests for search_pubmed function."""

    @patch('citation.requests.get')
    def test_search_successful(self, mock_get):
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "esearchresult": {"idlist": ["12345678"]}
        }
        mock_get.return_value = mock_response

        result = citation.search_pubmed("Test Title")
        assert result == "12345678"

    @patch('citation.requests.get')
    def test_search_not_found(self, mock_get):
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "esearchresult": {"idlist": []}
        }
        mock_get.return_value = mock_response

        result = citation.search_pubmed("Nonexistent Paper")
        assert result is None

    @patch('citation.requests.get')
    def test_search_timeout(self, mock_get):
        mock_get.side_effect = citation.requests.exceptions.Timeout()

        with pytest.raises(citation.APIError):
            citation.search_pubmed("Test")


class TestSearchCrossRef:
    """Tests for search_crossref function."""

    @patch('citation.requests.get')
    def test_search_successful(self, mock_get):
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "message": {"items": [{"DOI": "10.1234/example"}]}
        }
        mock_get.return_value = mock_response

        result = citation.search_crossref("Test Title")
        assert result == "10.1234/example"

    @patch('citation.requests.get')
    def test_search_not_found(self, mock_get):
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "message": {"items": []}
        }
        mock_get.return_value = mock_response

        result = citation.search_crossref("Nonexistent Paper")
        assert result is None


class TestGetCitation:
    """Tests for get_citation function."""

    @patch('citation.fetch_by_doi')
    def test_get_citation_by_doi(self, mock_fetch):
        mock_fetch.return_value = "@article{test}"

        result = citation.get_citation("10.1234/example", verbose=False)
        assert result == "@article{test}"
        mock_fetch.assert_called_once_with("10.1234/example")

    @patch('citation.fetch_by_pmid')
    def test_get_citation_by_pmid(self, mock_fetch):
        mock_fetch.return_value = "@article{test}"

        result = citation.get_citation("12345678", verbose=False)
        assert result == "@article{test}"
        mock_fetch.assert_called_once()

    @patch('citation.search_crossref')
    @patch('citation.fetch_by_doi')
    def test_get_citation_by_title(self, mock_fetch_doi, mock_search_crossref):
        mock_search_crossref.return_value = "10.1234/example"
        mock_fetch_doi.return_value = "@article{test}"

        result = citation.get_citation("Test Paper Title", verbose=False)
        assert result == "@article{test}"

    def test_get_citation_empty_query(self):
        result = citation.get_citation("", verbose=False)
        assert result is None


class TestProcessBatch:
    """Tests for process_batch function."""

    @patch('citation.get_citation')
    def test_process_multiple_queries(self, mock_get_citation):
        mock_get_citation.side_effect = [
            "@article{paper1}",
            "@article{paper2}",
            None
        ]

        results = citation.process_batch(
            ["Paper 1", "Paper 2", "Paper 3"],
            show_progress=False
        )

        assert len(results) == 3
        assert results[0][1] == "@article{paper1}"
        assert results[1][1] == "@article{paper2}"
        assert results[2][1] is None


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
