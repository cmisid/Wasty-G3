
# Groupe 3.
# V1.0.1
# modifications pour respect de la charte et correction de bug


import urllib.request
import urllib.parse
import simplejson
import json

answer = 'oui'

# Boucle globale pour ne sortir du programme qu'à la demande de l'utilisateur
while answer == 'oui':
    # La saisie du mot clé dont on veut récuperer les données sur data.toulouse
    search = input("Que voulez-vous rechercher ? Je suis a votre service (enfin data.toulouse, pas moi )\n")

    query = urllib.parse.urlencode({'q': search})
# Récuperation de l'url de l'API
    url = 'https://data.toulouse-metropole.fr/api/datasets/1.0/search/?%s' % query
# Ouverture de l'url
    research = urllib.request.urlopen(url)
# Chargement de la base de données dans une variable content
    content = simplejson.loads(research.read())
# Récuperation du nombre des datasets existant
    nbset = content['nhits']
    setlist = []
    nb_records = []
# Récuperation du titre de chaque dataset
    for i in range(0, nbset):
        setlist.append(content['datasets'][i]['metas']['title'])
# Récuperation du nombre d'enregistrements dans chaque dataset
    for i in range(0, nbset):
        nb_records.append(content['datasets'][i]['metas']['records_count'])
# Si on trouve aucun dataset relatif au mot clé recherché
    if nbset == 0:
        print(" Je ne trouve rien ! Voulez-vous essayer avec un autre mot clé ?")
        answer = input("Repondez par oui ou non \n")
# Refaire la recherche(la boucle globale) dés le debut ou sortir du programme
    else:
        answer = 'non'

        print("J'ai trouvé " + str(nbset) + " datasets : \n")
# Affichage des métadonnées de chaque dataset à savoir : sa description, le nombre de ses enregistrements et son index dans la liste
        for i in range(0, len(setlist)):
            print(str(i) + '- ' + setlist[i] + ' avec ' + str(nb_records[i]) + ' enregistrements' + '\n')
            print("\t" + content['datasets'][i]['metas']['description'] + "\n")
        print("Voulez-vous télécharger les données ?")
# Saisie des index des datasets voulus , le numero ou "all" pour tout les datasets et "no" sinon
        download = input("Donner le chiffre associé a ce que vous voulez télécharger : de 0 à " + str(nbset) + ". Ecrivez 'all' pour tout télécharger et 'no' pour ne rien télécharger \n")

        if download == 'no':
            print("OK, tant pis ! ciao")
# Téléchargement de tous les datasets
        elif download == 'all':
            for i in range(0, nbset):
                query = content['datasets'][int(i)]['datasetid']
                url = "https://data.toulouse-metropole.fr/api/records/1.0/search/?dataset=%s" % query
                search = urllib.request.urlopen(url)
                research = simplejson.loads(search.read())
                with open('%s.json' % query, 'w', encoding='utf8') as json_file:
                    json.dump(research, json_file, ensure_ascii=False)
# Téléchargement d'un dataset précis
        else:
            with_query = input("Voulez vous filtrer les recherches ? Repondez par oui ou non\n")
            if with_query == 'oui':
                # Filtre du dataset par  mot clé
                request = input("Quel est votre filtre?\n")
                query = content['datasets'][int(download)]['datasetid']
                url = "https://data.toulouse-metropole.fr/api/records/1.0/search/?dataset=%s&q=%s" % (query, request)
                print(url)
                search = urllib.request.urlopen(url)

                content = simplejson.loads(search.read())

                nbset = content['nhits']
                print("votre fichier filtré contient " + str(nbset) + " enregistrements")
                answer_download = input("Voulez-vous le telecharger ?\n")
                if answer_download == 'oui':
                    file = query+"avec-filtre-"+request
# Enregistrement du fichier json
                    with open('%s.json' % file, 'w', encoding='utf8') as json_file:
                        json.dump(content, json_file, ensure_ascii=False)
                else:
                    ask = input("d'accord, recherchez autre chose alors ? \n")
                    if ask == "oui":
                        answer = "oui"
                    else:
                        print("d'accord! A la prochaine :) ")
            else:
                query = content['datasets'][int(download)]['datasetid']
                url = "https://data.toulouse-metropole.fr/api/records/1.0/search/?dataset=%s" % query
                search = urllib.request.urlopen(url)
                content = simplejson.loads(search.read())
                with open('%s.json' % query, 'w', encoding='utf8') as json_file:
                    json.dump(content, json_file, ensure_ascii=False)
