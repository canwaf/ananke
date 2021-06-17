# download.py
from SPARQLWrapper import SPARQLWrapper, JSON

def get_endpoint() -> str:
    """
    Fetches the endpoint used in this utility.

    Returns:
        url (str): the endpoint url
    """
    return "https://staging.gss-data.org.uk/sparql"

def get_datasets(endpoint: str) -> list:
    return