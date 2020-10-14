import csv
from pprint import pprint
import os
import requests
from knora import Knora, Sipi
server = "http://0.0.0.0:3333"
#user = "root@example.com"
user = "tdk0805import@example.com"
password = "test"
projectcode = "0805"
ontoname = "tdk_onto"

con = Knora(server)
con.login(user, password)
sipi = Sipi("http://0.0.0.0:1024", con.get_token())


graph = con.get_ontology_graph(projectcode, ontoname)
schema = con.create_schema(projectcode, ontoname)
json = {"lageNr": "1234", "lageGrab" : 10, "lageUmgebung": "Umgebung", "lageAreal": "Areal", "lageRaum": "Raum", "lageSchnitt" : "Schnitt"}
result = con.create_resource(schema, "Lage", "test_resource",
                                                          json)
pprint(result)


