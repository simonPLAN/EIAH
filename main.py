import json
from datetime import datetime, date, timedelta
import statistics
import re
from datetime import datetime
from decimal import Decimal


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
            fln = trace.get('filePath','')
            if fln not in listExo and fln != '':
                if re.search(".*.c", fln):
                    listExo.append(fln)

        # Récupération uniquememnt des user étudiants (les profs n'ont pas de chiffre dans leur users)
    return listExo

# def tauxReussite(etu,exo,fichier):
#     truc={}
#     status = ""
#     tauxreussite = 0
#
#     total=0
#     res = 0
#
#     for trace in fichier:
#         #    "timestamp": "2022-10-20T06:46:18.217Z",
#         tmpdate = datetime.strptime('2000-10-20T06:46:18.217Z','%Y-%m-%dT%H:%M:%S.%fZ')
#
#         args = trace.get('args')
#         if trace.get('username') == etu and trace.get('args').find(exo) and trace.get('command') == "gcc":
#             newdate = datetime.strptime(trace.get('timestamp'), '%Y-%m-%dT%H:%M:%S.%fZ')
#             if tmpdate - newdate < timedelta(seconds=1):
#                 tmpdate = newdate
#
#         if trace.get('response') == "":
#             status = "OK"
#             tauxreussite = tauxreussite + 1
#         else:
#             status = "error"
#
#             total = total + 1
#
#             truc2 = {exo: status}
#
#             truc.update(truc2)
#
#         if tauxreussite > 0:
#             res = tauxreussite/total*100
#
#
#     return truc, res


def tauxReussite(etu, listExo):
    fichier = lectureJson("662cfbebea6d4042934526197165d805_instructions.json")

    tabfinal = {}
    tauxreussite = 0
    total = 0
    resTaux = 0


    for exo in listExo:

        tmpdate = datetime.strptime('2000-10-20T06:46:18.217Z', '%Y-%m-%dT%H:%M:%S.%fZ')
        exoS = exo.split("/")
        for trace in fichier:
            args = trace.get('args').split(" ")

            if trace.get('username') == etu and args.count(exoS[-1]) > 0 and trace.get('command') == "gcc":

                newdate = datetime.strptime(trace.get('timestamp'), '%Y-%m-%dT%H:%M:%S.%fZ')

                if (newdate > tmpdate):
                    #
                    # print(exoS[-1])
                    # print("NEW DATE = ", newdate)
                    # print("TMP DATE = ", tmpdate)
                    tmpdate = newdate

        # print(nomEtu)
        # print(exo)
        # print(tmpdate)

        for trace in fichier:
            actueldate = datetime.strptime(trace.get('timestamp'), '%Y-%m-%dT%H:%M:%S.%fZ')
            # print("TMP DATE", tmpdate)
            # print("DATE REEL",actuelDate)

            if trace.get('username') == etu and trace.get('args').find(exoS[-1])  and trace.get('command') == "gcc" and actueldate == tmpdate:
                if trace.get('response') == "":
                    tabtmp = {exo: "OK"}
                    tauxreussite = tauxreussite + 1
                else:
                    tabtmp = {exo: "error"}

                tabfinal.update(tabtmp)

    if tauxreussite > 0 and len(listExo) > 0:

        resTaux = tauxreussite / len(listExo) * 100

    return tabfinal, round(resTaux)

if __name__ == '__main__':
    data = []


    fichier_in = lectureJson("662cfbebea6d4042934526197165d805_instructions.json")
    fichier_vm = lectureJson("662cfbebea6d4042934526197165d805_vmInteractions.json")

    listeEtu = listUser(fichier_vm)

    truc = {}

    for nomEtu in listeEtu:
        listReussite = []
        listExo = listExoUser(nomEtu, fichier_vm)
        val,tauxR = tauxReussite(nomEtu,listExoUser(nomEtu, fichier_vm))
        # listReussite.append(val)
        # truc2 = {
        print(val)
        print('TauxR' , tauxR)
        # }
        # truc.update(truc2)

    #print(truc)

    ecrireJson(data, "etuInfo")


"""    etudiant = {
            "username": nomEtu,
            "listExo": listExoUser(nomEtu,fichier_vm),
            "nbExo": len(listExoUser(nomEtu,fichier_vm)),
            "taux_reussite": "10"
        }
        data.append(etudiant)

        for nomExo in listExoUser(nomEtu,fichier_vm):
            tab.append(tauxReussite(nomEtu,nomExo, fichier_in))


        print(tab) """


   # ecrireJson(data, "etuInfo")