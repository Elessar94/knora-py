import os
from typing import List, Set, Dict, Tuple, Optional
from pprint import pprint
import argparse
import json
from jsonschema import validate
from knora import KnoraError, KnoraStandoffXml, Knora, Sipi


parser = argparse.ArgumentParser()
parser.add_argument("-s", "--server", type=str, default="http://0.0.0.0:3333", help="URL of the Knora server")
parser.add_argument("-S", "--sipi", type=str, default="http://0.0.0.0:1024", help="URL of SIPI server")
parser.add_argument("-u", "--user", default="root@example.com", help="Username for Knora")
parser.add_argument("-p", "--password", default="test", help="The password for login")
parser.add_argument("-P", "--projectcode", default="00FE", help="Project short code")
parser.add_argument("-O", "--ontoname", default="kpt", help="Shortname of ontology")

args = parser.parse_args()


con = Knora(args.server)
con.login(args.user, args.password)

graph = con.get_ontology_graph(args.projectcode, args.ontoname)
# print(graph)
# exit(0)
schema = con.create_schema(args.projectcode, args.ontoname)
# pprint(schema)
# exit(0)


inst1_info = con.create_resource(schema, "object1", "obj1_inst1", {
    "textprop": "Dies ist ein Text!",
    "intprop": 7,
    "listprop": "options:opt2",
    "dateprop": "1966:CE:1967-05-21",
    "decimalprop": {'value': "3.14159", 'comment': "Die Zahl PI"},
    "geonameprop": "2661604",
    "richtextprop": {
        'value': KnoraStandoffXml("<?xml version=\"1.0\" encoding=\"UTF-8\"?>\n<text><p><strong>this is</strong> text</p> with standoff</text>"),
        'comment': "Text mit markup"
    },
    "intervalprop": "13.57:15.88"
})
pprint(inst1_info)

#first upload image to SIPI
sipi = Sipi(args.sipi, con.get_token())
res = sipi.upload_image('example.tif')
pprint(res)

fileref = res['uploadedFiles'][0]['internalFilename']
inst2_info = con.create_resource(schema, "object2", "obj2_inst1", {
    "titleprop": "Stained glass",
    "linkprop": inst1_info['iri']
}, fileref)
pprint(inst2_info)
