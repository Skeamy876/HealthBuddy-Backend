import requests
import logging

# Set up logging for 'requests'
logging.basicConfig(level=logging.DEBUG)
logging.getLogger('urllib3').setLevel(logging.DEBUG)

def icd10_search_tool(query: str) -> str:
    """
    Search for ICD-10 codes based on a query string.
    Returns a string with the search results.
    """
    # Placeholder for actual ICD-10 search logic
    # In a real implementation, this would query an ICD-10 database or API
    url = "https://clinicaltables.nlm.nih.gov/api/icd10cm/v3/search"
    params = {
        "terms": query,
        "sf": "name",
        "df": "code",
    }

    resp = requests.get(url, params=params)
    resp.raise_for_status()
    print(resp.json())
    payload = resp.json()
    # payload[1] is a list of codes when df="code"
    codes = payload[1]

    if not codes:
        return f"No ICD-10‑CM codes found for '{query}'."

    # Format codes as a Python list literal
    codes_list = ", ".join(codes)
    return f"ICD-10 codes for '{query}': [{codes_list}]"
