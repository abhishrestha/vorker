import requests
from bs4 import BeautifulSoup
from google.adk.tools import FunctionTool


def search_swedish_sources(query: str) -> str:
    """
    Search authoritative Swedish government sites for regulatory information.
    Returns snippets AND a list of URLs to fetch for full content.
    
    Args:
        query: The search query in Swedish or English
    Returns:
        Relevant text snippets with source URLs to fetch next
    """
    sources = {
        "skatteverket": f"https://www.skatteverket.se/sok?q={query.replace(' ', '+')}",
        "verksamt": f"https://www.verksamt.se/sok?query={query.replace(' ', '+')}",
    }
    
    # Known high-quality direct pages for common topics
    direct_pages = {
        "karensavdrag": "https://www.skatteverket.se/privat/skatter/arbeteochinkomst/formaner/sjukersattningochandraersattningar/karensavdrag.4.22501d9e166a8e8d25288b9.html",
        "moms": "https://www.skatteverket.se/foretag/moms.html",
        "vat": "https://www.skatteverket.se/foretag/moms.html",
        "aktiebolag": "https://bolagsverket.se/foretag/aktiebolag.html",
        "aktieägaravtal": "https://bolagsverket.se/foretag/aktiebolag/startaaktiebolag/aktieagaravtal.html",
        "hembudsförbehåll": "https://bolagsverket.se/foretag/aktiebolag/startaaktiebolag/aktieagaravtal.html",
    }
    
    results = []
    headers = {"User-Agent": "Mozilla/5.0 (compatible; VorkerAgent/1.0)"}
    
    # Check if query matches a known direct page
    for keyword, url in direct_pages.items():
        if keyword.lower() in query.lower():
            results.append(f"IMPORTANT: Fetch this URL immediately for authoritative content: {url}")
    
    for source_name, url in sources.items():
        try:
            r = requests.get(url, headers=headers, timeout=5)
            soup = BeautifulSoup(r.text, "html.parser")
            paragraphs = soup.find_all("p")
            text = " ".join(p.get_text() for p in paragraphs[:5])
            results.append(f"[{source_name}] {text[:600]}\nFetch for full content: {url}")
        except Exception as e:
            results.append(f"[{source_name}] Could not fetch: {e}")
    
    return "\n\n".join(results) + "\n\nNOTE: You MUST now call fetch_official_page on the most relevant URL above."

def fetch_official_page(url: str) -> str:
    """
    Fetches the full text of a specific official Swedish government page.
    Use when you know the exact URL of a relevant law or regulation.
    
    Args:
        url: Full URL of the page (must be .se government domain)
    Returns:
        Cleaned text content of the page
    """
    allowed_domains = [
        "skatteverket.se", "bolagsverket.se", "verksamt.se",
        "riksdagen.se", "arbetsmiljoverket.se", "tillvaxtverket.se"
    ]
    
    if not any(domain in url for domain in allowed_domains):
        return "Error: Only Swedish government domains are allowed."
    
    headers = {"User-Agent": "Mozilla/5.0 (compatible; VorkerAgent/1.0)"}
    try:
        r = requests.get(url, headers=headers, timeout=8)
        soup = BeautifulSoup(r.text, "html.parser")
        
        # Remove nav, footer, scripts
        for tag in soup(["script", "style", "nav", "footer", "header"]):
            tag.decompose()
        
        text = soup.get_text(separator="\n", strip=True)
        return text[:3000]  # cap tokens
    except Exception as e:
        return f"Error fetching page: {e}"


# Wrap as ADK tools
search_tool = FunctionTool(search_swedish_sources)
fetch_tool = FunctionTool(fetch_official_page)