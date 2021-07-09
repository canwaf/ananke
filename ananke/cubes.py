from abc import ABC, abstractmethod
from download import *

class Component(ABC):
    url: str


    def __init__(self, url: str):
        self.url = url

        # get the labels

    def get_component_metadata(self):
        pass
        

    def label(self):
        get_sparql(f"""
        
        
        """)
        pass

    

class Dimension(Component):

    def __init__(self, url: str):
        pass

    pass

class DataSet(ABC):

