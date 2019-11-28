import csv
from pprint import pprint
import os
import re
from knora import Knora, Sipi
server = "http://0.0.0.0:3333"
user = "root@example.com"
password = "test"
projectcode = "0805"
ontoname = "tdk_onto"

con = Knora(server)
con.login(user, password)
sipi = Sipi("http://0.0.0.0:1024", con.get_token())


graph = con.get_ontology_graph(projectcode, ontoname)
schema = con.create_schema(projectcode, ontoname)

subdirectory = "tdk_Data"
lage_file = "tdk_Lage.csv"
kampagne_file = "tdk_Kampagne.csv"
zeichnung_file = "tdk_Zeichnungen.csv"
pub_file = "tdk_Publikation.csv"
smfund_file = "tdk_SMFUND.csv"
bild_file = "tdk_Bilder.csv"


class tdk_create_data:
    def __init__(self):
        self.lage_store = {}
        self.kampagne_store = {}
        self.zeichnung_store = {}
        self.pub_store = {}
        self.smfund_store = {}
        self.bild_store = {}

    def create_lage(self, lage_file):
        listsep = ','
        with open(self.get_file(lage_file)) as csvfile:
            count = 0
            csvreader = csv.reader(csvfile, delimiter=';', quotechar='"')
            for line in csvreader:
                for i in range(len(line)):

                    if line[i].find(listsep) != -1:
                        line[i] = line[i].split(listsep)
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


                self.lage_store[line[0]] = con.create_resource(schema, "Lage", "LAGE_" + str(line[0]),
                                                          json)['iri']
                count = count + 1

                pprint(count)


    def create_kampagne(self, kampagne_file):
        listsep = '/'
        with open(self.get_file(kampagne_file), encoding='utf-8') as csvfile:

            csvreader = csv.reader(csvfile, delimiter=';', quotechar='"')
            null = next(csvreader)
            for line in csvreader:
                line[1] = self.getDate(line[1])
                line[2] = self.getDate(line[2])

                for i in range(len(line)):
                    if line[i].find(listsep) != -1:
                        line[i] = line[i].split(listsep)

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
                pprint(json)
                self.kampagne_store[line[0]] = con.create_resource(schema, "Kampagne", "KAMPAGNE_" + str(line[0]),
                                                              json)['iri']

    def create_bild(self, bild_file):
        listsep = '/'
        with open(bild_file, encoding='utf-8') as csvfile:
            csvreader = csv.reader(csvfile, delimiter=';', quotechar='"')
            null = next(csvreader)
            for line in csvreader:
                line[1] = self.getDate(line[1])
                line[2] = self.getDate(line[2])
                for i in range(len(line)):
                    if line[i].find(listsep) != -1:
                        line[i] = line[i].split(listsep)
                        json = {}
                    if not line[0] == "":
                        json["bildDateiname"] = line[0]
                    #if not line[2] == "":
                            #json["bildLage"] = line[2]  #TODO
                    if not line[3] == "":
                        json["bildKampagne"] = line[3] #TODO
                    if not line[4] == "":
                        json["bildDatum"] = self.getDate(line[4])
                    if not line[5] == "":
                        json["bildAbhub"] = line[7]
                    if not line[6] == "":
                        json["bildGefaessNr"] = line[6]
                    if not line[6] == "":
                        json["bildMaskenNr"] = line[6]
                    if not line[6] == "":
                        json["bildKartonageNr"] = line[6]
                    if not line[6] == "":
                        json["bildAnthropologieNr"] = line[6]
                    if not line[6] == "":
                        json["bildAutor"] = line[6]


                self.bild_store[line[0]] = con.create_resource(schema, "Kampagne", "KAMPAGNE_" + str(line[0]),
                                                              {"kampagne": line[0], "kampagneStartDatum": line[1],
                                                               "kampagneEndDatum": line[2],
                                                               "kampagneTeilnehmer": line[3], "kampagneGrab": line[4],
                                                               "kampagneUmgebung": line[5],
                                                               "kampagneBemerkung": line[6]})['iri']


    def create_zeichnungen(self, zeichnung_file):
        listsep = "&"
        zeichnung_dir = "tdk_Data/zeichnungen/"
        with open(self.get_file(zeichnung_file), encoding='utf-8') as csvfile:

            csvreader = csv.reader(csvfile, delimiter=';', quotechar='"')
            null = next(csvreader)
            for line in csvreader:

                for i in range(len(line)):
                    if line[i].find(listsep) != -1:
                        line[i] = line[i].split(listsep)

                json = {}
                if not line[0] == "":
                    json["zeichnungNr"] = line[0]
                if not line[1] == "":
                    json["zeichnungDatum"] = self.getDate(line[1])
                #if not line[3] == "":
                    #json["zeichnungKampagne"] = line[3]
                if not line[3] == "":
                    json["zeichnungBemerkung"] = line[3]
                if not line[4] =="":
                    or_file = zeichnung_dir +"Z_"+ line[4] + ".tif"
                    res = sipi.upload_image(or_file)
                    pprint(res)
                    file = res['uploadedFiles'][0]['internalFilename']

                pprint(json)
                self.zeichnung_store[line[4]] = con.create_resource(schema, "Zeichnung", "ZEICHNUNG_" + str(line[0]),
                                                              json, file)['iri']

    def create_smfund(self, smfund_file):
        listsep = '&'
        with open(self.get_file(smfund_file), encoding='utf-8') as csvfile:

            csvreader = csv.reader(csvfile, delimiter=';', quotechar='"')
            null = next(csvreader)
            done = 0
            for line in csvreader:

                for i in range(len(line)):
                    if line[i].find(listsep) != -1:
                        line[i] = line[i].split(listsep)
                json = {}
                if not line[0] == "":
                    json["smFundNr"] = line[0]

                if not line[1] == "":
                    json["smNr"] = line[1]

                if not line[2] == "":
                    json["fundNr"] = line[2]
                if not line[3] == "":
                    json["smGefaessNr"] = line[3]

                if not line[4] == "":
                    json["smMaskenNr"] = line[4]
                if not line[5] == "":
                    json["smKartonageNr"] = line[5]

                if not line[6] == "":
                    json["smGrab"] = line[6]

                if not line[7] == "":
                    json["smUmgebung"] = line[7]
                if not line[8] == "":
                    json["smAreal"] = line[8]
                if not line[9] == "":
                    json["smRaum"] = line[9]
                if not line[10] == "":
                    json["smAbhub"] = line[10]

                if not line[11] == "":
                    json["smSchnitt"] = line[11]
                if not line[13] == "":
                    json["smBefundVG"] = line[13]

                if not line[14] == "":
                    json["smBefundKommentar"] = line[14]

                if not line[15] == "":
                    json["smMaterial"] = self.get_listnode(line[15], "Material")
                if not line[16] == "":
                    json["smMaterialZusatz"] = self.get_listnode(line[16],"MaterialZusatz")
                if not line[17] == "":
                    json["smObjekttyp"] = self.get_listnode(line[17],"Objekttyp")
                if not line[18] == "":
                    json["smObjekttypZusatz"] = self.get_listnode(line[18],"ObjekttypZusatz")
                if not line[19] == "":
                    json["smDekoration"] = self.get_listnode(line[19],"Dekoration")
                if not line[20] == "":
                    json["smObjektbeschreibung"] = line[20]
                if not line[21] == "":
                    json["smAufschrift"] = line[21]

                if not line[22] == "":
                    json["smDatierung1"] = self.get_listnode(line[22],"DatierungOne")

                if not line[23] == "":
                    json["smDatierung2"] = self.get_listnode(line[23],"DatierungTwo")
                if not line[24] == "":
                    json["smHoehe"] = line[24]
                if not line[25] == "":
                    json["smBreite"] = line[25]
                if not line[26] == "":
                    json["smTiefe"] = line[26]
                if not line[27] == "":
                    json["smDurchm1"] = line[27]
                if not line[28] == "":
                    json["smDurchm2"] = line[28]
                if not line[29] == "":
                    json["smBrandspuren"] = self.get_listnode(line[29],"Brandspuren")
                if not line[30] == "":
                    json["smFeuchtigkeit"] = self.get_listnode(line[30],"Feuchtigkeit")

                check_for_drawing = []
                if isinstance(line[1], list):
                    for s in line[1]:
                        check_for_drawing.append(s)
                else:
                    check_for_drawing.append(line[1])
                if isinstance(line[2], list):
                    for s in line[2]:
                        check_for_drawing.append(s)
                else:
                    check_for_drawing.append(line[2])
                for s in check_for_drawing:
                    if s in self.zeichnung_store:
                        json["smZeichnung"] = self.zeichnung_store[s]
                pprint(json)
                self.smfund_store[line[0]] = con.create_resource(schema, "SMFund", "SMFUND_" + str(line[0]),
                                                         json)['iri']
                done = done + 1
                pprint(done)
    def create_publikation(self, pub_file):
        listsep = "&"
        with open(self.get_file(pub_file), encoding='utf-8') as csvfile:

            csvreader = csv.reader(csvfile, delimiter=';', quotechar='"')
            null = next(csvreader)
            for line in csvreader:

                for i in range(len(line)):
                    if line[i].find(listsep) != -1:
                        line[i] = line[i].split(listsep)

                json = {}
                if not line[0] == "":
                    json["publikationKurzzitat"] = line[0]

                if not line[1] == "":
                    json["publikationTitel"] = line[1]

                if not line[2] == "":
                    json["publikationAutor"] = line[2]
                if not line[3] == "":
                    json["publikationJahr"] = line[3]
                if not line[4] == "":
                    json["publikationWo"] = line[4]
                if not line[5] == "":
                    json["publikationLink"] = line[5]
                if not line[6] == "":
                    json["publikationZusammenfassung"] = line[6]
                #if not line[5] == "":
                    #json["publikationInhaltsverzeichnis"] = line[5]
                if not line[7] == "":
                    json["publikationStichwort"] = line[7]

                pprint(json)
                self.pub_store[line[0]] = con.create_resource(schema, "Publikation", "PUB_" + str(line[0]),
                                                              json)['iri']

    def create_backward_links(self):
        pass
    def getDate(self, str):
        str = str.split('.')
        if len(str)!=3:
            print(str)
            raise ValueError
        if len(str[2]) == 2:
            str[2] = "20" + str[2]
        str = str[2]+"-"+str[1]+"-"+str[0]
        return str

    def get_file(self, str):
        script_dir= os.path.dirname(__file__)
        rel_path = subdirectory + "/" + str
        return os.path.join(script_dir,rel_path)

    def get_listnode(self, str, l):
        if isinstance(str, list):
            output =[]
            for s in str:
                output.append(self.get_listnode(s, l))
            return output
        if l == "DatierungTwo" and  str[len(str)-1] == "D":
            str = str[:len(str) - 2] + "." + str[len(str) - 2:]
            str = str + "ynastie"
        if l == "DatierungTwo" and str[len(str) - 3:] == "Dyn":
            str = str[:len(str) - 4] + "." + str[len(str) - 3:]
            str = str + "astie"
        if l == "Objekttyp":
            if str == "Einlage":
                str = "Gefäss Einlage"
            if str == "Abdruck":
                str == "Abdruckobjekt"
        if l == "MaterialZusatz" and str == "Alabaster":
            str = "ägyptischer Alabaster"
        str = l + ":" + str[0].capitalize() + str[1:]
        return str.replace(" ", "")



c = tdk_create_data()
#c.create_lage(lage_file)
pprint("_______________________________________")
pprint("Done with LAGE")
pprint("_______________________________________")
#c.create_kampagne(kampagne_file)
pprint("_______________________________________")
pprint("Done with KAMPAGNE")
pprint("_______________________________________")
#c.create_zeichnungen(zeichnung_file)
pprint("_______________________________________")
pprint("Done with ZEICHNUNG")
pprint("_______________________________________")
#c.create_publikation(pub_file)
pprint("_______________________________________")
pprint("Done with PUBLIKATION")
pprint("_______________________________________")
#c.create_smfund(smfund_file)
pprint("_______________________________________")
pprint("Done with SMFUND")
pprint("_______________________________________")
c.create_bild(bild_file)
pprint("_______________________________________")
pprint("Done with BILD")
pprint("_______________________________________")
