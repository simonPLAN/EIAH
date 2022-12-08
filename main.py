import json
from datetime import datetime, date, timedelta
import statistics
import re
from datetime import datetime


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


def listUser(fichier):
    listEtu = []
    for i in range(len(fichier)):
        etu = fichier[i]['username']
        # Récupération uniquememnt des user étudiants (les profs n'ont pas de chiffre dans leur users)
        if etu not in listEtu:
            if re.search(".*[0-9].*", etu):
                listEtu.append(etu)
    return listEtu


def listExoUser(etu,fichier):
    listExo = []

    for trace in fichier:
        if trace.get('username') == etu:
            fln = trace.get('fileName','')
            if fln not in listExo and fln != '':
                if re.search(".*.c", fln):
                    listExo.append(fln)

        # Récupération uniquememnt des user étudiants (les profs n'ont pas de chiffre dans leur users)
    return listExo

def tauxReussite(etu,exo,fichier):

    for trace in fichier:
        #    "timestamp": "2022-10-20T06:46:18.217Z",
        tmp = datetime.strptime('2000-10-20T06:46:18.217Z','%Y-%m-%dT%H:%M:%S.%fZ')

        if trace.get('username') == etu and trace.get('fileName') == exo and trace.get('command') == "gcc":
            tmpZZZ = datetime.strptime(trace.get('timestamp'), '%Y-%m-%dT%H:%M:%S.%fZ')
            if tmp - tmpZZZ < timedelta(seconds=1):
                tmp = tmpZZZ
            if trace.get('response') == "":
                status = "OK"
            else:
                status = "error"

    return tmp,status



if __name__ == '__main__':
    data = []


    fichier_in = lectureJson("662cfbebea6d4042934526197165d805_instructions.json")
    fichier_vm = lectureJson("662cfbebea6d4042934526197165d805_vmInteractions.json")

    listeEtu = listUser(fichier_vm)
    tab = []
    for nomEtu in listeEtu:
        etudiant = {
            "username": nomEtu,
            "listExo": listExoUser(nomEtu,fichier_vm),
            "nbExo": len(listExoUser(nomEtu,fichier_vm)),
            "taux_reussite": "10"
        }
        data.append(etudiant)

        for nomExo in listExoUser(nomEtu,fichier_vm):
            tab.append(tauxReussite(nomEtu,nomExo, fichier_in))


        print(tab)


   # ecrireJson(data, "etuInfo")

