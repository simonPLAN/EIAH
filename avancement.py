from datetime import datetime, date, timedelta
import re
from dataclasses import dataclass

import statut as s
import tauxReussite as tr
import main as m


def listGCC(etudiant, tabdate, nomexo):
    data = m.lectureJson("662cfbebea6d4042934526197165d805_instructions.json")
    tab = []
    for date in range(len(tabdate)):
        datedebut = datetime.strptime(tabdate[date][0], '%Y-%m-%dT%H:%M:%S.%fZ')
        datefin = datetime.strptime(tabdate[date][1], '%Y-%m-%dT%H:%M:%S.%fZ')
        for i in range(len(data)):
            if data[i]['username'] == etudiant:
                if data[i]['command'] == "gcc":
                    dategcc = datetime.strptime(data[i]['timestamp'], '%Y-%m-%dT%H:%M:%S.%fZ')
                    if datedebut < dategcc < datefin:
                        test = str(nomexo).split("/")
                        if test[-1] in data[i]['args']:
                            gcc = {
                                "timestamp": data[i]['timestamp'],
                                "responce": data[i]['response'],
                                "score": data[i]['score'],
                                "replicate": data[i]['replicate']
                            }
                            tab.append(gcc)
    return tab

"""
def listUser():
    fichier = m.lectureJson("662cfbebea6d4042934526197165d805_vmInteractions.json")
    listEtu = []
    for i in range(len(fichier)):
        etu = fichier[i]['username']
        # Récupération uniquememnt des user étudiants (les profs n'ont pas de chiffre dans leur users)
        if etu not in listEtu:
            if re.search(".*[0-9].*", etu):
                listEtu.append(etu)
    return listEtu
"""

@dataclass
class doubleret():
    tab: list
    nbseance: int


def rechercheseance(etudiant):
    data = m.lectureJson("662cfbebea6d4042934526197165d805_vmInteractions.json")
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
    global test
    test = "null"

    listeexerciceReturn = []
    for exo in listeExoUser:

        gcc = listGCC(nomEtu, date, exo)
        if not gcc:
            test = "liste vide"
        else:
            for i in gcc:
                test = str(i['responce'])

                if test != "":

                    if test.__contains__("error"):
                        test2 = test.split("error: ")
                        test = test2
                    if test.__contains__("warning"):
                        test2 = test.split("warning: ")
                        test = test2

                if test == "":
                    test = "exoFini"
                else:
                    test = "probleme"
        exercice = {
            "nomExercice": exo,
            "statut": "a faire",
            "gcc": gcc,
            "error": test
        }
        listeexerciceReturn.append(exercice)

    return listeexerciceReturn


def getInfoSeance(tabdate, listeExoUser, nomEtu):
    returne = []
    for i in range(len(tabdate)):
        avancementEtu = {
            "dateDebut": tabdate[i][0],
            "dateFin": tabdate[i][1],
            "exercice": getavancementexercice(listeExoUser, nomEtu, i, tabdate),
            "tauxReussite": tr.tauxReussite(nomEtu, listeExoUser)

        }
        returne.append(avancementEtu)
    return returne


def generationIndicateurs () :
    data = []
    fichier_vm = m.lectureJson("662cfbebea6d4042934526197165d805_vmInteractions.json")
    listeEtu = m.listUser(fichier_vm)

    listTraceInteraction = []
    for nomEtu in listeEtu:
        print(nomEtu)
        listeExoUser = m.listExoUser(nomEtu, fichier_vm)
        date = rechercheseance(nomEtu)
        x = getseance(date)
        tabdate = x.tab
        nbseance = x.nbseance

        #Récupération des traces propre à chacun des utilisateurs
        tracesUser = []
        for ligne in fichier_vm:
            if ligne["username"] == nomEtu:
                tracesUser.append(ligne)
        listTraceInteraction.append(tracesUser)

        #Récupération des informations pour chaque étudiant
        etudiant = {
            "username": nomEtu,
            "nbseance": nbseance,
            "seance": getInfoSeance(tabdate, listeExoUser, nomEtu)
        }
        data.append(etudiant)

    m.ecrireJson(data, "avancement")

    #Définition du statut d'avancement de chaque exercice pour chaque séance pour chaque étudiant
    for nomEtu, traces in zip(listeEtu, listTraceInteraction):
        s.statutEtu(nomEtu, traces)