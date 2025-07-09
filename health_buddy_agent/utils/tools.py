import requests
import logging
from google.ai.generativelanguage_v1beta.types import Tool as GenAITool

# Set up logging for 'requests'
logging.basicConfig(level=logging.DEBUG)
logging.getLogger('urllib3').setLevel(logging.DEBUG)

def icd10_search_tool(query: str) -> str:
    """
    Search for ICD-10 codes based on a query string.
    Returns a string with the search results.
    """
    url = "https://clinicaltables.nlm.nih.gov/api/icd10cm/v3/search"
    params = {
        "terms": query,
        "sf": "name",
        "df": "code",
    }

    try:
        resp = requests.get(url, params=params)
        resp.raise_for_status()
        payload = resp.json()

        # Check if the response is in the expected format
        if not isinstance(payload, list) or len(payload) < 2:
            return f"Unexpected API response format for '{query}'."

        codes = payload[1]

        if not codes:
            return f"No ICD-10‑CM codes found for '{query}'."

        # Format codes as a Python list literal
        codes_list = ", ".join(codes)
        return f"ICD-10 codes for '{query}': [{codes_list}]"

    except requests.exceptions.RequestException as e:
        return f"An error occurred while searching for ICD-10 codes: {e}"
