import csv
from pprint import pprint
import os
import re
from knora import Knora
server = "http://0.0.0.0:3333"
user = "root@example.com"
password = "test"
projectcode = "0805"
ontoname = "tdk_onto"

con = Knora(server)
con.login(user, password)


graph = con.get_ontology_graph(projectcode, ontoname)
schema = con.create_schema(projectcode, ontoname)

subdirectory = "tdk_Data"
lage_file = "tdk_Lage.csv"
kampagne_file = "tdk_Kampagne.csv"


class tdk_create_data:

    def create_lage(self, lage_file):
        lage_store = {}  # stores iris in format {lageNr  : iri}
        with open(self.get_file(lage_file)) as csvfile:
            count = 0
            for line in csv.reader(csvfile, delimiter=';', quotechar='"'):
                for i in range(len(line)):

                    if line[i].find(",") != -1:
                        line[i] = line[i].split(",")
                        line[i] = list(dict.fromkeys(line[i]))


                json = {"lageNr": line[0]}
                if not line[1] == "":
                    json["lageGrab"] = line[1]
                if not line[2] == "":
                    json["lageUmgebung"] = line[2]
                if not line[3] == "":
                    json["lageAreal"] = line[3]
                if not line[4] == "":
                    json["lageRaum"] = line[4]
                if not line[5] == "":
                    json["lageSchnitt"] = line[5]


                lage_store[line[0]] = con.create_resource(schema, "Lage", "LAGE_" + str(line[0]),
                                                          json)['iri']
                count = count + 1

                pprint(count)

        return lage_store

    def create_kampagne(self, kampagne_file):
        kampagne_store = {}
        with open(self.get_file(kampagne_file), encoding='utf-8') as csvfile:
            count = 0
            for line in csv.reader(csvfile, delimiter=';', quotechar='"'):
                line[1] = self.getDate(line[1])
                line[2] = self.getDate(line[2])

                for i in range(len(line)):
                    if line[i].find("/") != -1:
                        line[i] = line[i].split("/")

                json = {"kampagne" : line[0]}
                if not line[1] == "":
                    json["kampagneStartDatum"] = line[1]
                if not line[2] == "":
                    json["kampagneEndDatum"] = line[2]
                if not line[3] == "":
                    json["kampagneTeilnehmer"] = line[3]
                if not line[4] == "":
                    json["kampagneGrab"] = line[4]
                if not line[5] == "":
                    json["kampagneUmgebung"] = line[5]
                if not line[6] == "":
                    json["kampagneBemerkung"] = line[6]
                kampagne_store[line[0]] = con.create_resource(schema, "Kampagne", "KAMPAGNE_" + str(line[0]),
                                                              json)['iri']

                count = count + 1
                pprint(count)
    def create_bild(self, bild_file):
        bild_store = {}
        with open(bild_file, encoding='utf-8') as csvfile:
            for line in csv.reader(csvfile, delimiter=';', quotechar='"'):
                line[1] = self.getDate(line[1])
                line[2] = self.getDate(line[2])
                for i in range(len(line)):
                    if line[i].find("/") != -1:
                        line[i] = line[i].split("/")

                bild_store[line[0]] = con.create_resource(schema, "Kampagne", "KAMPAGNE_" + str(line[0]),
                                                              {"kampagne": line[0], "kampagneStartDatum": line[1],
                                                               "kampagneEndDatum": line[2],
                                                               "kampagneTeilnehmer": line[3], "kampagneGrab": line[4],
                                                               "kampagneUmgebung": line[5],
                                                               "kampagneBemerkung": line[6]})['iri']

    def getDate(self, str):
        #TODO implement this using regular expressions
        str = str.split('.')
        if len(str)!=3:
            raise ValueError
        str = str[2]+"-"+str[1]+"-"+str[0]
        return str

    def get_file(self, str):
        script_dir= os.path.dirname(__file__)
        rel_path = subdirectory + "/" + str
        return os.path.join(script_dir,rel_path)


c = tdk_create_data()
#c.create_lage(lage_file) #TODO here a logout error gets thrown
c.create_kampagne(kampagne_file)
