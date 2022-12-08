import json
from datetime import datetime, date, timedelta
import statistics
import re
from dataclasses import dataclass
# Lecture du fichier JSON
def lectureJson(nomFichier):
    fileObject = open(nomFichier, "r")
    jsonContent = fileObject.read()
    aList = json.loads(jsonContent)
    fileObject.close()
    return aList


# Ecriture de la list de dictionnaire dans le fichier JSON
def ecrireJson(data, nomFichier):
    with open(nomFichier + '.json', 'w') as mon_fichier:
        json.dump(data, mon_fichier, indent=2)


#def listGCC(etudiant):
 #   data = lectureJson("662cfbebea6d4042934526197165d805_instructions.json")
  #  for i in range(len(data)):
   #     if data[i]['username'] == etudiant:
    #        if data[i]['command'] == "gcc":


def listUser():
    fichier = lectureJson("662cfbebea6d4042934526197165d805_vmInteractions.json")
    listEtu = []
    for i in range(len(fichier)):
        etu = fichier[i]['username']
        # Récupération uniquememnt des user étudiants (les profs n'ont pas de chiffre dans leur users)
        if etu not in listEtu:
            if re.search(".*[0-9].*", etu):
                listEtu.append(etu)
    return listEtu



@dataclass
class doubleret():
    datedebut:str
    datefin:str


def rechercheseance(etudiant):
    data= lectureJson("662cfbebea6d4042934526197165d805_vmInteractions.json")
    date=[]
    for i in data:
        if i['username'] == etudiant:
            date.append(i['timestamp'])
    return date
    #return doubleret("1","2")


def getseance(date):
    seuilTemp=
    timeline=[]
    for i in date:
        print(i)





if __name__ == '__main__':
    data = []

    listeEtu = listUser()

    for nomEtu in listeEtu:
        date=rechercheseance(nomEtu)
        yes=getseance(date)


        debutseance,finseance
        seance = {
            "debutSeance":debutseance,
            "finSeance":finseance,
            "numseance": "yes"
        }
        etudiant = {
            "username": nomEtu,
            "exercice": [seance]
        }
        data.append(etudiant)

    ecrireJson(data, "etuInfo")

    print(listeEtu)
