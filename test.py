import json
from datetime import datetime, date, timedelta
import statistics
import re


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


"""def listGCC(etudiant):
    data = lectureJson("662cfbebea6d4042934526197165d805_instructions.json")
    for i in range(len(data)):
        if data[i]['username']== etudiant:
            if data[i]['command'] == "gcc": """


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


def listExoUser(etu):
    fichier = lectureJson("662cfbebea6d4042934526197165d805_vmInteractions.json")
    listExo = []

    for trace in fichier:
        print(trace.get('fileName'))
        listExo.append(trace.get('fileName'))
        # Récupération uniquememnt des user étudiants (les profs n'ont pas de chiffre dans leur users)
    return listExo


if __name__ == '__main__':
    data = []

    listeEtu = listUser()

    fichier = lectureJson("662cfbebea6d4042934526197165d805_vmInteractions.json")

    for nomEtu in listeEtu:
        etudiant = {
            "username": nomEtu,
            "listExo": "listExoUser(nomEtu)"
        }
        data.append(etudiant)

    ecrireJson(data, "etuInfo")

