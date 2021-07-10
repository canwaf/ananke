# download.py
import pandas as pd
import hashlib
import sqlite3

from datetime import datetime

from SPARQLWrapper import SPARQLWrapper, JSON


def get_endpoint() -> str:
    """
    Fetches the endpoint used in this utility, returns the JSON type

    Returns:
        url (str): the endpoint url
    """

    sparql = SPARQLWrapper("https://beta.gss-data.org.uk/sparql")

    sparql.setReturnFormat(JSON)

    return sparql


def get_sparql(query_text: str) -> pd.DataFrame:
    """
    Queries the set SPARQL endpoint the given query_text or returns a sqlite3
    cached version. It creates a new sqlite3 database per SPARQL endpoint, and
    there is no cache expiry. If you want to fetch fresh data, delete the
    database. Soz.

    Parameters:
        query_text (str): a SPARQL query

    Returns:
        results (DataFrame): the results in a pandas DataFrame.
    """
    # Really bad caching, but I digress
    query_hex = hashlib.sha224(query_text.encode()).hexdigest()
    endpoint_hex = hashlib.sha224(get_endpoint().endpoint.encode()).hexdigest()

    # find the database connection
    con = sqlite3.connect(f"{endpoint_hex}.db")

    # check if the query_hex exists
    exist_query = (
        f"SELECT count(*) FROM sqlite_master WHERE type='table' AND name='{query_hex}';"
    )
    exist_result = bool(con.execute(exist_query).fetchone()[0])  # 0 = False

    if exist_result:
        # results exist so fetch results
        df = pd.read_sql(f"SELECT * FROM [{query_hex}]", con=con)
    else:
        # results don't exist in db so get them from SPARQL
        sparql = get_endpoint()
        sparql.setQuery(query_text)
        results = sparql.queryAndConvert()

        # normalise the json results
        df = pd.json_normalize(results["results"]["bindings"])

        # store the results in db
        df.to_sql(query_hex, con)

        # log the query
        record = {
            "hash": [query_hex],
            "query": [query_text],
            "timestamp": [datetime.now().strftime("%Y-%m-%d %H:%M:%S")],
        }
        pd.DataFrame.from_dict(record, orient="columns").to_sql(
            "manifest", con, if_exists="append", index=False
        )

    return df


def get_datasets() -> dict:
    """
    Function to get the datasets (i.e. qb:cubes) for the SPARQL endpoint.

    Returns:
        results (DataFrame): The list of qb:Cubes on a SPARQL endpoint.
    """

    query = """PREFIX pmdcat: <http://publishmydata.com/pmdcat#>
PREFIX dcterms: <http://purl.org/dc/terms/>

# Select details regarding all datasets, assume that if there's a catalog entry
# there is an associated dataset. Might be good to check if the GRAPH exists.

SELECT ?graphUrl ?catUrl ?datasetUrl ?catTitle ?catDesc 
WHERE {
	?catUrl pmdcat:graph ?graphUrl ;
              dcterms:title ?catTitle ;
              dcterms:description ?catDesc ;
              pmdcat:datasetContents ?datasetUrl .

}"""

    return get_sparql(query)


def get_components(graph_uri: str):
    """
    Function to get the list qb:componentProperty for a given graph containing a qb:cube.

    Arguments:
        graph_uri (str): string URI of for the graph containing the qb:cube

    Returns:
        results (DataFrame): The components of a qb:Cube
    """

    query = f"""PREFIX qb: <http://purl.org/linked-data/cube#>
PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>

# For a given cube's graph, select its components

SELECT ?graphUrl ?component ?kind ?definition
WHERE {{
    BIND(<{graph_uri}> as ?graphUrl) .
    GRAPH  ?graphUrl {{
        ?component qb:componentProperty ?definition .
        ?definition rdf:type ?kind .
    }}

}}"""

    return get_sparql(query)


# Compare dimensions
# Want to use urllib's object model to get the fragments of a url to find out
# things like the componentProperty type
# urllib.parse.urlparse(json_normalize(components).loc[3, 'kind.value'])
# > ParseResult(scheme='http', netloc='purl.org', path='/linked-data/cube', params='', query='', fragment='AttributeProperty')
# Also want to use urllib to extract the path, to get the dimension name
