#!/usr/bin/env python3
"""
Citation Grabber - Fetch scientific paper citations from multiple sources.

This module provides functionality to search and retrieve citations in BibTeX
or NBIB format from PubMed and CrossRef databases.
"""

import sys
import requests
import argparse
import re
import logging
from typing import Optional, List, Tuple
from urllib.parse import quote_plus
from pathlib import Path

# --- Constants ---
CROSSREF_API = "https://api.crossref.org/works"
NCBI_SEARCH_URL = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi?db=pubmed&retmode=json&term={}"
NCBI_FETCH_URL = "https://api.ncbi.nlm.nih.gov/lit/ctxp/v1/pubmed/?format={}&id={}"

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(message)s',
    handlers=[logging.StreamHandler(sys.stderr)]
)
logger = logging.getLogger(__name__)


class CitationError(Exception):
    """Base exception for citation-related errors."""
    pass


class APIError(CitationError):
    """Exception raised when API requests fail."""
    pass


class NotFoundError(CitationError):
    """Exception raised when a citation cannot be found."""
    pass


def detect_type(query: str) -> str:
    """
    Detect the type of query (DOI, PMID, or title).

    Args:
        query: The search query string

    Returns:
        One of 'doi', 'pmid', or 'title'

    Examples:
        >>> detect_type("10.1234/example")
        'doi'
        >>> detect_type("12345678")
        'pmid'
        >>> detect_type("Attention Is All You Need")
        'title'
    """
    query = query.strip()

    # DOI Pattern: 10.xxxx/yyyy
    if re.search(r'10\.\d{4,}/[-._;()/:a-zA-Z0-9]+', query):
        return 'doi'

    # PMID Pattern: Pure digits, usually 8 chars or less
    if re.match(r'^\d{1,10}$', query):
        return 'pmid'

    return 'title'


def fetch_by_doi(doi: str) -> Optional[str]:
    """
    Fetch citation by DOI from doi.org.

    Args:
        doi: Digital Object Identifier

    Returns:
        BibTeX citation string or None if not found

    Raises:
        APIError: If the API request fails
    """
    try:
        headers = {"Accept": "application/x-bibtex; charset=utf-8"}
        url = f"https://doi.org/{doi}"
        resp = requests.get(url, headers=headers, timeout=10)

        if resp.status_code == 200:
            logger.info(f"✓ Found via DOI: {doi}")
            return f"% Source: DOI ({doi})\n{resp.text}"
        elif resp.status_code == 404:
            logger.warning(f"DOI not found: {doi}")
            return None
        else:
            logger.warning(f"DOI lookup failed with status {resp.status_code}")
            return None

    except requests.exceptions.Timeout:
        logger.error(f"Timeout while fetching DOI: {doi}")
        raise APIError(f"Timeout while fetching DOI: {doi}")
    except requests.exceptions.RequestException as e:
        logger.error(f"Error fetching DOI {doi}: {e}")
        raise APIError(f"Error fetching DOI: {e}")


def fetch_by_pmid(pmid: str, fmt: str = 'bibtex') -> Optional[str]:
    """
    Fetch citation by PubMed ID.

    Args:
        pmid: PubMed ID
        fmt: Output format ('bibtex' or 'nbib')

    Returns:
        Citation string in requested format or None if not found

    Raises:
        APIError: If the API request fails
    """
    api_fmt = 'nbib' if fmt == 'nbib' else 'bibtex'

    try:
        url = NCBI_FETCH_URL.format(api_fmt, pmid)
        resp = requests.get(url, timeout=10)

        if resp.status_code == 200:
            logger.info(f"✓ Found via PMID: {pmid}")
            return f"% Source: PubMed (PMID: {pmid})\n{resp.text}"
        elif resp.status_code == 404:
            logger.warning(f"PMID not found: {pmid}")
            return None
        else:
            logger.warning(f"PubMed lookup failed with status {resp.status_code}")
            return None

    except requests.exceptions.Timeout:
        logger.error(f"Timeout while fetching PMID: {pmid}")
        raise APIError(f"Timeout while fetching PMID: {pmid}")
    except requests.exceptions.RequestException as e:
        logger.error(f"Error fetching PMID {pmid}: {e}")
        raise APIError(f"Error fetching PMID: {e}")


def search_pubmed(title: str) -> Optional[str]:
    """
    Search for a paper in PubMed by title.

    Args:
        title: Paper title to search

    Returns:
        PubMed ID if found, None otherwise

    Raises:
        APIError: If the API request fails
    """
    try:
        url = NCBI_SEARCH_URL.format(quote_plus(title))
        resp = requests.get(url, timeout=10)
        resp.raise_for_status()

        data = resp.json()
        id_list = data.get("esearchresult", {}).get("idlist", [])

        if id_list:
            return id_list[0]
        return None

    except requests.exceptions.Timeout:
        logger.error(f"Timeout while searching PubMed for: {title}")
        raise APIError(f"Timeout while searching PubMed")
    except requests.exceptions.RequestException as e:
        logger.error(f"Error searching PubMed: {e}")
        raise APIError(f"Error searching PubMed: {e}")
    except (KeyError, ValueError) as e:
        logger.error(f"Error parsing PubMed response: {e}")
        raise APIError(f"Error parsing PubMed response: {e}")


def search_crossref(title: str) -> Optional[str]:
    """
    Search for a paper in CrossRef by title.

    Args:
        title: Paper title to search

    Returns:
        DOI if found, None otherwise

    Raises:
        APIError: If the API request fails
    """
    try:
        params = {'query.title': title, 'rows': 1}
        resp = requests.get(CROSSREF_API, params=params, timeout=10)
        resp.raise_for_status()

        data = resp.json()
        items = data.get("message", {}).get("items", [])

        if items:
            return items[0].get("DOI")
        return None

    except requests.exceptions.Timeout:
        logger.error(f"Timeout while searching CrossRef for: {title}")
        raise APIError(f"Timeout while searching CrossRef")
    except requests.exceptions.RequestException as e:
        logger.error(f"Error searching CrossRef: {e}")
        raise APIError(f"Error searching CrossRef: {e}")
    except (KeyError, ValueError) as e:
        logger.error(f"Error parsing CrossRef response: {e}")
        raise APIError(f"Error parsing CrossRef response: {e}")


def get_citation(query: str, fmt: str = 'bibtex', verbose: bool = True) -> Optional[str]:
    """
    Get citation for a query (title, DOI, or PMID).

    This is the main entry point for fetching citations. It automatically
    detects the query type and uses the appropriate search strategy.

    Args:
        query: Search query (title, DOI, or PMID)
        fmt: Output format ('bibtex' or 'nbib')
        verbose: Whether to print progress messages

    Returns:
        Citation string if found, None otherwise

    Raises:
        APIError: If API requests fail
    """
    query = query.strip()
    if not query:
        logger.warning("Empty query provided")
        return None

    qtype = detect_type(query)

    if verbose:
        logger.info(f"🔍 Processing: {query[:60]}{'...' if len(query) > 60 else ''} (Type: {qtype})")

    try:
        # Strategy 1: Direct DOI
        if qtype == 'doi':
            return fetch_by_doi(query)

        # Strategy 2: Direct PMID
        if qtype == 'pmid':
            return fetch_by_pmid(query, fmt)

        # Strategy 3: Title Search
        # If user specifically wants NBIB (PubMed format), try PubMed search first
        if fmt == 'nbib':
            pmid = search_pubmed(query)
            if pmid:
                return fetch_by_pmid(pmid, fmt)

        # Default: Try CrossRef search for DOI (Best for BibTeX)
        doi = search_crossref(query)
        if doi:
            return fetch_by_doi(doi)

        # Fallback: If CrossRef failed, try PubMed search
        pmid = search_pubmed(query)
        if pmid:
            return fetch_by_pmid(pmid, fmt)

        logger.warning(f"❌ No citation found for: {query}")
        return None

    except APIError as e:
        logger.error(f"❌ API Error for '{query}': {e}")
        return None


def process_batch(
    inputs: List[str],
    fmt: str = 'bibtex',
    show_progress: bool = True
) -> List[Tuple[str, Optional[str]]]:
    """
    Process multiple citation queries in batch.

    Args:
        inputs: List of queries to process
        fmt: Output format ('bibtex' or 'nbib')
        show_progress: Whether to show progress information

    Returns:
        List of (query, citation) tuples
    """
    results = []
    total = len(inputs)

    for i, query in enumerate(inputs, 1):
        if show_progress:
            logger.info(f"\n[{i}/{total}] Processing...")

        citation = get_citation(query, fmt, verbose=show_progress)
        results.append((query, citation))

    return results


def main():
    """Main entry point for the command-line interface."""
    parser = argparse.ArgumentParser(
        description="Fetch citations (BibTeX/NBIB) from Title, DOI, or PMID.",
        epilog="Examples:\n"
               "  %(prog)s \"Attention Is All You Need\"\n"
               "  %(prog)s 10.1234/example --format bibtex\n"
               "  %(prog)s papers.txt --output references.bib\n",
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    parser.add_argument(
        "input",
        help="Title, DOI, PMID, or path to .txt file with multiple queries"
    )
    parser.add_argument(
        "--format",
        choices=["bibtex", "nbib"],
        default="bibtex",
        help="Output format (default: bibtex)"
    )
    parser.add_argument(
        "--output", "-o",
        help="Output file path (default: print to stdout)"
    )
    parser.add_argument(
        "--quiet", "-q",
        action="store_true",
        help="Suppress progress messages"
    )
    parser.add_argument(
        "--version",
        action="version",
        version="%(prog)s 1.1.0"
    )

    args = parser.parse_args()

    # Set logging level
    if args.quiet:
        logger.setLevel(logging.ERROR)

    # Determine input queries
    input_path = Path(args.input)
    if input_path.is_file():
        try:
            with open(input_path, 'r', encoding='utf-8') as f:
                inputs = [line.strip() for line in f if line.strip()]
            logger.info(f"📂 Loaded {len(inputs)} queries from file.")
        except IOError as e:
            logger.error(f"❌ Error reading file: {e}")
            sys.exit(1)
    else:
        inputs = [args.input]

    # Process queries
    results = process_batch(inputs, args.format, show_progress=not args.quiet)

    # Collect successful citations
    citations = []
    failed_count = 0

    for query, citation in results:
        if citation:
            citations.append(citation)
        else:
            failed_count += 1

    # Output results
    if citations:
        output_text = "\n\n".join(citations)

        if args.output:
            try:
                output_path = Path(args.output)
                output_path.write_text(output_text, encoding='utf-8')
                logger.info(f"\n✅ Saved {len(citations)} citation(s) to {args.output}")
            except IOError as e:
                logger.error(f"❌ Error writing output file: {e}")
                sys.exit(1)
        else:
            print(output_text)

    # Summary
    if not args.quiet and len(inputs) > 1:
        logger.info(f"\n📊 Summary: {len(citations)}/{len(inputs)} successful")
        if failed_count > 0:
            logger.info(f"   {failed_count} failed")

    # Exit with error code if all queries failed
    if failed_count == len(inputs):
        sys.exit(1)


if __name__ == "__main__":
    main()
