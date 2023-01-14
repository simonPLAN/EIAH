import main as m

import matplotlib.pyplot as plt
import numpy as np
from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_score

#Récupère les indicateurs présents dans avancement.json et les mets sous forme de vecteur pour chaque utilisateur
def getDataClustering ():
    vecteur = []

    fichier_av = m.lectureJson("avancement.json")
    for user in fichier_av:
        vecteurPersonne = []
        nbSeance = 0
        cptRef = 0
        cptDev = 0
        cptDebug = 0
        cptEnd = 0
        tauxDeResussite = 0
        difficulteSeance = 0
        for j in user['seance']:
            cptProbleme = 0
            #Indicateur : nombre séance
            nbSeance+=1
            #Indicateur : taux de réussite
            tauxDeResussite = +j['tauxReussite'][1]
            #Indicateur : statut exercice fin séance
            exercice = j['exercice']
            for o in exercice:
                if o['statut'] == 'reflexion':
                    cptRef += 1
                if o['statut'] == 'dev':
                    cptDev += 1
                if o['statut'] == 'termine':
                    cptEnd += 1
                if o['statut'] == 'debug':
                    cptDebug += 1
                if o['error'] == 'probleme':
                    cptProbleme += 1
            # Indicateur : élève en difficulté
            if cptProbleme >= 1:
                difficulteSeance += 1

        if nbSeance == 0 :
            nbSeance = 1
        moyRef = cptRef/nbSeance
        moyDev = cptDev/nbSeance
        moyDebug = cptDebug/nbSeance
        moyEnd = cptEnd/nbSeance
        nbStatutMoy = moyRef + moyDev + moyDebug + moyEnd
        if nbStatutMoy == 0 :
            nbStatutMoy = 1
        #Ajout des indicateurs dans le vecteur de l'utiilisateur
        vecteurPersonne.append(tauxDeResussite)
        vecteurPersonne.append(moyRef/nbStatutMoy)
        vecteurPersonne.append(moyDev/nbStatutMoy)
        vecteurPersonne.append(moyDebug/nbStatutMoy)
        vecteurPersonne.append(moyEnd/nbStatutMoy)
        vecteurPersonne.append(difficulteSeance/nbSeance)
        vecteurPersonne.append(nbSeance)
        #Ajout du vecteur de l'utilisateur dans le vecteur final
        vecteur.append(vecteurPersonne)

    data = np.array(vecteur)
    print(data)
    return data

#Récupère le nombre de cluster le plus adaptés aux donnés (score silhouetteà
def getNbCluster (data) :
    kmeans_kwargs = {
        "init": "random",
        "n_init": 10,
        "max_iter": 300,
        "random_state": 42,
    }

    silhouette_coefficients = []
    for k in range(2, 11):
        kmeans = KMeans(n_clusters=k, **kmeans_kwargs)
        kmeans.fit(data)
        score = silhouette_score(data, kmeans.labels_)
        silhouette_coefficients.append(score)
    #print(silhouette_coefficients)
    nbCluster = silhouette_coefficients.index(max(silhouette_coefficients))+2
    print(nbCluster)

    #Affichage du score silhouette
    #plt.style.use("fivethirtyeight")
    plt.plot(range(2, 11), silhouette_coefficients)
    plt.xticks(range(2, 11))
    plt.xlabel("Number of Clusters")
    plt.ylabel("Silhouette Coefficient")
    plt.show()

    return nbCluster

#Génération des clusters via Kmeans
def clustering_Kmeans (data, nbCluster):
    modelKmeans = KMeans(n_clusters=nbCluster, random_state=0).fit(data)
    for point in data:
        if modelKmeans.predict(point.reshape(1, -1)) == [0]:
            plt.scatter(point[0], point[1], c='b')
        elif modelKmeans.predict(point.reshape(1, -1)) == [1]:
            plt.scatter(point[0], point[1], c='g')
        elif modelKmeans.predict(point.reshape(1, -1)) == [2]:
            plt.scatter(point[0], point[1], c='r')
        elif modelKmeans.predict(point.reshape(1, -1)) == [3]:
            plt.scatter(point[0], point[1], c='y')

    #Affichage des centroïdes
    for x, center in enumerate(modelKmeans.cluster_centers_):
        if x == 0 :
            color = 'b'
        elif x == 1 :
            color = 'g'
        elif x == 2 :
            color = 'r'
        else :
            color = 'y'
        plt.scatter(center[0], center[1], marker="x", c=color)
    plt.show()
