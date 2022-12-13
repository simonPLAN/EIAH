import json
from datetime import datetime, date, timedelta
import statistics
import re
from dataclasses import dataclass

from main import listExoUser


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


def listGCC(etudiant, tabdate, nomexo):
    data = lectureJson("662cfbebea6d4042934526197165d805_instructions.json")
    tab = []
    for date in range(len(tabdate)):
        datedebut = datetime.strptime(tabdate[date][0], '%Y-%m-%dT%H:%M:%S.%fZ')
        datefin = datetime.strptime(tabdate[date][1], '%Y-%m-%dT%H:%M:%S.%fZ')
        for i in range(len(data)):
            if data[i]['username'] == etudiant:
                if data[i]['command'] == "gcc":
                    dategcc = datetime.strptime(data[i]['timestamp'], '%Y-%m-%dT%H:%M:%S.%fZ')
                    if datedebut < dategcc < datefin:
                        print(data[i]['args'])
                        print(nomexo)

                        if nomexo in data[i]['args']:
                            gcc = {
                                "timestamp": data[i]['timestamp'],
                                "responce": data[i]['response'],
                                "score": data[i]['score'],
                                "replicate": data[i]['replicate']
                            }
                            tab.append(gcc)
    return tab


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
    tab: list
    nbseance: int


def rechercheseance(etudiant):
    data = lectureJson("662cfbebea6d4042934526197165d805_vmInteractions.json")
    date = []
    for i in data:
        if i['username'] == etudiant:
            date.append(i['timestamp'])
    return date
    # return doubleret("1","2")


def getseance(date):
    nbseance = 0
    tab = []
    tabseance = []

    date1 = datetime.strptime(date[0], '%Y-%m-%dT%H:%M:%S.%fZ')
    for i in date:
        date2 = datetime.strptime(i, '%Y-%m-%dT%H:%M:%S.%fZ')
        if date2 - date1 < timedelta(hours=1):
            tabseance.append(i)
            date1 = date2
        else:
            tabb = []
            if tabseance:
                tabb.append(tabseance[0])
                tabb.append(tabseance[len(tabseance) - 1])
                tab.append(tabb)
                tabseance.clear()
            date1 = date2

            nbseance = nbseance + 1
    return doubleret(tab, nbseance)


def getavancementexercice(listeExoUser, nomEtu, i, date):
    listeexerciceReturn = []

    for exo in listeExoUser:
        exercice = {
            "nomExercice": exo,
            "statut": "a faire",
            "gcc": listGCC(nomEtu, date, exo)
        }
        listeexerciceReturn.append(exercice)

    return listeexerciceReturn


def getInfoSeance(tabdate, listeExoUser, nomEtu):
    returne = []
    for i in range(len(tabdate)):
        avancementEtu = {
            "dateDebut": tabdate[i][0],
            "dateFin": tabdate[i][1],
            "exercice": getavancementexercice(listeExoUser, nomEtu, i, tabdate)
        }
        returne.append(avancementEtu)
    return returne


if __name__ == '__main__':
    data = []

    listeEtu = listUser()

    for nomEtu in listeEtu:
        print(nomEtu)
        fichier_vm = lectureJson("662cfbebea6d4042934526197165d805_vmInteractions.json")
        listeExoUser = listExoUser(nomEtu, fichier_vm)
        tabdate = []
        date = rechercheseance(nomEtu)
        x = getseance(date)
        tabdate = x.tab
        nbseance = x.nbseance

        etudiant = {
            "username": nomEtu,
            "nbseance": nbseance,
            "seance": getInfoSeance(tabdate, listeExoUser, nomEtu)
        }
        data.append(etudiant)

    ecrireJson(data, "avancement")

    print(listeEtu)
