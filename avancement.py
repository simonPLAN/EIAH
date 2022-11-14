import json
from datetime import datetime, date, timedelta
import statistics


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
        json.dump(data, mon_fichier)


def getgcc():
    data = lectureJson("662cfbebea6d4042934526197165d805_instructions.json")
    for i in range(len(data)):
        if data[i]['command'] == "gcc":


def listUser():
    fichier = lectureJson("662cfbebea6d4042934526197165d805_vmInteractions.json")
    listEtu = []
    for i in range(len(fichier)):
        etu = fichier[i]['username']
        if etu not in listEtu:
            listEtu.append(etu)
    return listEtu


if __name__ == '__main__':
    data = []

    listeEtu = listUser()
    for nomEtu in listeEtu:
        etudiant = {
            "username": nomEtu,
            "gcc": listGCC(nomEtu),
        }
    data.append(etudiant)
