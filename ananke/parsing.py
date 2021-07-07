import pandas as pd

from urllib.parse import urlparse


def get_fragment(url: str) -> str:
    """Function to parse a url when you can't depend on the fragment
    being the component of the property you want.

    Parameters:
        url (str): the url you want to parse

    Returns:
        fragment (str): the final part of a parsed url
    """

    parsed = urlparse(url)

    if len(parsed.fragment) == 0:
        return parsed.path.split("/")[-1]
    elif "/" in parsed.fragment:
        return parsed.fragment.split("/")[-1]
    else:
        return parsed.fragment


def get_dimensions(components: pd.DataFrame) -> list:
    """Function to returns a list of dimensions in a given dataset's components

    Parameters:
        components (pd.DataFrame): a dataframe from get_components()

    Returns:
        dimensions (list): a list of dimensions by name
    """

    dimensions = components.loc[
        components["kind.value"].apply(lambda x: get_fragment(x))
        == "DimensionProperty",
        "definition.value",
    ]

    return list(dimensions.apply(lambda x: get_fragment(x)))