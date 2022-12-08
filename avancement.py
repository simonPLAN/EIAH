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
    nbseance=0
    tab=[]
    tabseance = []

    date1 = datetime.strptime(date[0], '%Y-%m-%dT%H:%M:%S.%fZ')
    for i in date:
        date2 = datetime.strptime(i, '%Y-%m-%dT%H:%M:%S.%fZ')
        if date2-date1 <timedelta(hours=1):
            tabseance.append(i)
            date1=date2
        else:
            tabb=[]
            tabb.append(tabseance[0])
            tabb.append(tabseance[len(tabseance)-1])

            tab.append(tabb)
            tabseance.clear()
            date1=date2

            nbseance=nbseance+1
    print(tab)
    return nbseance






if __name__ == '__main__':
    data = []

    listeEtu = listUser()

    for nomEtu in listeEtu:
        print(nomEtu)

        date=rechercheseance(nomEtu)
        nbseance=getseance(date)
        etudiant = {
            "username": nomEtu,
            "nbseance": nbseance
        }
        data.append(etudiant)

    ecrireJson(data, "etuInfo")

    print(listeEtu)
