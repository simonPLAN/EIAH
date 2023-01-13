import main as m

import matplotlib.pyplot as plt
import numpy as np
from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_score

#Récupère les indicateurs présents dans avancement.json et les mets sous forme de vecteur pour chaque utilisateur
def getDataClustering ():
    vecteur = []

    fichier_vm = m.lectureJson("avancement.json")
    for i in fichier_vm:
        vecteurPersonne = []
        nbSeance = 0
        cptRef = 0
        cptDev = 0
        cptDebug = 0
        cptEnd = 0
        cptProbleme = 0
        tauxDeResussite = 0
        for j in i['seance']:
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
        if nbSeance == 0 :
            nbSeance = 1
        #Ajout des indicateurs dans le vecteur de l'utiilisateur
        vecteurPersonne.append(tauxDeResussite)
        vecteurPersonne.append(cptRef/nbSeance)
        vecteurPersonne.append(cptDev/nbSeance)
        vecteurPersonne.append(cptDebug/nbSeance)
        vecteurPersonne.append(cptEnd/nbSeance)
        vecteurPersonne.append(nbSeance)
        #Indicateur : élève en difficulté
        if cptProbleme >= 1:
            error = 1
        else:
            error = 0
        vecteurPersonne.append(error)
        #Ajout du vecteur de l'utilisateur dans le vecteur final
        vecteur.append(vecteurPersonne)

    data = np.array(vecteur)
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

    #Affichage du score silhouette
    plt.style.use("fivethirtyeight")
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
