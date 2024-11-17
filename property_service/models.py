from google.cloud import datastore
from dataclasses import dataclass, asdict

@dataclass
class Property:
    nom : str
    description : str
    type_de_bien : str
    ville : str 
    pieces : list = None
    proprietaire : str


