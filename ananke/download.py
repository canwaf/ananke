# download.py
import pandas as pd

from SPARQLWrapper import SPARQLWrapper, JSON, CSV

def get_endpoint() -> str:
    """
    Fetches the endpoint used in this utility, returns the JSON type

    Returns:
        url (str): the endpoint url
    """

    sparql = SPARQLWrapper("https://staging.gss-data.org.uk/sparql")

    sparql.setReturnFormat(JSON)

    return  sparql

def json_to_df(results_json: dict) -> pd.DataFrame():
    return pd.json_normalize(results_json['results']['bindings'])

def get_datasets() -> dict:
    """
    Function to get the datasets (i.e. qb:cubes) for the SPARQL endpoint.

    Returns:
        json (dict): SPARQL endpoint response, not normalised
    """

    query = \
"""
PREFIX pmdcat: <http://publishmydata.com/pmdcat#>
PREFIX dcterms: <http://purl.org/dc/terms/>

# Select details regarding all datasets, assume that if there's a catalog entry
# there is an associated dataset. Might be good to check if the GRAPH exists.

SELECT ?graphUrl ?catUrl ?datasetUrl ?catTitle ?catDesc 
WHERE {
	?catUrl pmdcat:graph ?graphUrl ;
              dcterms:title ?catTitle ;
              dcterms:description ?catDesc ;
              pmdcat:datasetContents ?datasetUrl .

}
"""

    sparql = get_endpoint()
    sparql.setQuery(query)
    results = sparql.queryAndConvert()

    return results

def get_components(graph_uri: str):
    """
    Function to get the list qb:componentProperty for a given graph containing a qb:cube.

    Arguments:
        graph_uri (str): string URI of for the graph containing the qb:cube

    Returns:
        json (dict): SPARQL endpoint response, not normalised
    """

    query = \
f"""
PREFIX dcat: <http://www.w3.org/ns/dcat#>
PREFIX pmdcat: <http://publishmydata.com/pmdcat#>
PREFIX dcterms: <http://purl.org/dc/terms/>
PREFIX owl: <http://www.w3.org/2002/07/owl#>
PREFIX qb: <http://purl.org/linked-data/cube#>
PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
PREFIX skos: <http://www.w3.org/2004/02/skos/core#>
PREFIX void: <http://rdfs.org/ns/void#>
PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>

# For a given cube's graph, select its components

SELECT ?graphUrl ?component ?kind ?definition
WHERE {{
    BIND(<{graph_uri}> as ?graphUrl) .
    GRAPH  ?graphUrl {{
        ?component qb:componentProperty ?definition .
        ?definition rdf:type ?kind .
    }}

}}
"""

    sparql = get_endpoint()
    sparql.setQuery(query)
    results = sparql.queryAndConvert()

    return results

# Compare dimensions
# Want to use urllib's object model to get the fragments of a url to find out
# things like the componentProperty type
# urllib.parse.urlparse(json_normalize(components).loc[3, 'kind.value'])
# > ParseResult(scheme='http', netloc='purl.org', path='/linked-data/cube', params='', query='', fragment='AttributeProperty')
# Also want to use urllib to extract the path, to get the dimension name
