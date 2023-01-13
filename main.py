import json
import re

import avancement as av
import clustering as c

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


if __name__ == '__main__':
    #av.generationIndicateurs()
    data = c.getDataClustering()
    nbCluster = c.getNbCluster(data)
    c.clustering_Kmeans(data, nbCluster)