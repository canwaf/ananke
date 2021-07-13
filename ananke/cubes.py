from abc import ABC
import datetime

from ananke.download import get_sparql
from typing import List, Tuple
from pandas import DataFrame

class Component(ABC):
    """ Basic class of components of the structure of a Cube.

    uri (str) - the uri of the component
    label (str) - the human readable label
    type (str) - the type of component (qb spec)
    """

    def __init__(self, url: str):
        self.url: str = url
        self.label: str
        self.type: str

        # get the labels
        pass

    def _get_component_metadata(self):
        pass


class Attribute(Component):
    """ An attribute is a component with no associated links, specific to the dataset.
    
    """

    # Check if the URI provided is infact an Attribute

    pass
    

class Dimension(Component):
    """ A dimension is a component of the dataset which can be linked to other datasets.
    
    dimension (str) - the uri of the dimension
    subPropertyOf (str) - the parent linked data uri (normally refArea/refPeriod)
    codelist (dict) - the dictionary of the codelist {code: human readable}
    """
    def __init__(self, url: str):
        self.dimension: str
        self.subPropertyOf: str
        self.codelist: dict
    
        # Check if the URI provided is infact an Dimension

    def _get_component_metadata(self):
        pass

class Dataset(ABC):
    def __init__(self, url: str):
        self.url: str = url

        # Metadata
        self.title: str # DCAT
        self.description: str # DCAT

        self.issued: datetime # DCAT
        self.modified: datetime # DCAT

        self.publisher: str # DCAT
        self.creator: str # DCAT
        self.comment: str # DCAT

        self.components: List[Dimension, Attribute] # QB 
        self.data: DataFrame # QB

        # Check if the URI provided is infact a DataSet

    def size(self) -> Tuple[int,int]:
        pass

    def materialise(self):
        pass

    def compare(self, other: Dataset):
        pass

    def describe(self):
        pass

    def slice(self, fixed=List, common=str, observations=str) -> DataFrame:
        pass

    def _get_data(self):
        pass
    
    def _get_structure(self):
        pass

