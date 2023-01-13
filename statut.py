from datetime import datetime, date, timedelta
import avancement as av


def statutEtu(nomEtu, interactionsUser):
    fichiersEtu = []
    print(nomEtu)
    # Réupération données avancement.json de l'étudiant
    avancementEtu = None
    avancementFile = av.lectureJson("avancement.json")
    for a in avancementFile:
        if a["username"] == nomEtu:
            avancementEtu = a
            break
    # Détermination du statut d'un exercice pour chaque interaction
    for inter in interactionsUser:
        if "filePath" in inter:
            cheminFichier = inter["filePath"]
            #print(cheminFichier)
            date = inter["timestamp"].replace("T", " ")
            horaire = datetime.strptime(date[:-5], '%Y-%m-%d %H:%M:%S')

            #print(inter["action"])
            # Création d'un nouveau fichier
            if inter["action"] == "editFileOpen":
                statut = "reflexion"
                getExoSeanceUser(cheminFichier, horaire, avancementEtu, statut, avancementFile)

            # Modification d'un fichier existant
            elif inter["action"] == "editFileChange":
                statut = "dev"
                getExoSeanceUser(cheminFichier, horaire, avancementEtu, statut, avancementFile)

            # Sauvegarde d'un fichier
            elif inter["action"] == "saveFile":
                statut = None
                getExoSeanceUser(cheminFichier, horaire, avancementEtu, statut, avancementFile)


# Retourne le numéro de la séance concerné dans le avancement.json
def getSeanceWithDate(date, userSeances):
    for x, seance in enumerate(userSeances):
        dateDebut = datetime.strptime(seance["dateDebut"][:-5], '%Y-%m-%dT%H:%M:%S')
        dateFin = datetime.strptime(seance["dateFin"][:-5], '%Y-%m-%dT%H:%M:%S')
        #print(date, dateDebut, dateFin)
        if date >= dateDebut and date < (dateFin + timedelta(minutes=15)):
            return x
    return None


def getExoSeanceUser(cheminFichier, date, avancementUser, statut, avancementFile):
    userSeances = avancementUser["seance"]
    indexSeance = getSeanceWithDate(date, userSeances)
    #print(indexSeance, statut)
    if indexSeance != None:
        seance = userSeances[indexSeance]
        exercices = seance["exercice"]  # Récupération des exercices
        # Parcours des exos
        for exo in exercices:
            # Récupération du bon exercice
            if cheminFichier == exo["nomExercice"]:
                if exo["statut"] != "termine":
                    if statut == None:  # Statut non déterminé
                        #print(exo["error"])
                        if exo["error"] == "exoFini":
                            statut = "termine"
                        else:
                            statut = commandeGcc(exo, date)
                            # pas de gcc
                            if statut == None:
                                if exo["statut"] != "a faire":
                                    break
                                else:
                                    statut = "dev"

                    #print("Statut", statut)
                    exo["statut"] = statut
                    av.ecrireJson(avancementFile, "avancement")


def commandeGcc(exo, date):
    listGcc = exo["gcc"]  # Récupération des gcc
    if listGcc:
        # Parcours des gcc
        for x, gcc in enumerate(listGcc):
            dateGCC = datetime.strptime(gcc["timestamp"][:-5], '%Y-%m-%dT%H:%M:%S')
            if dateGCC >= date or x == len(listGcc) - 1:
                if gcc["score"] == 0 and gcc["replicate"] == True:
                    return "debug"
                else:
                    return "dev"
    return None
