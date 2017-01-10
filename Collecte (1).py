"""
Ce script est une interaction homme machine qui permet à un utilisateur de télécharger les données depuis data.toulouse selon ses demandes
Le script tourne autant de temps que veut l'utilisateur , la boucle est controlée par la variable "rep" ('oui' ==> Script tourne , 'non' sinon )
L'utilisateur doit entrer un mot clé pour pouvoir récuperer les datasets qui ont une relation avec
Le script permet à l'utilisateur de voir le titre et le nombre d'enregistrements de chaque dataset généré


"""



from bs4 import BeautifulSoup
import urllib.request
import urllib.parse
import simplejson
import requests



rep='oui'
#Boucle globale pour ne sortir du programme qu'à la demande de l'utilisateur
while rep=='oui':
#La saisie du mot clé dont on veut récuperer les données sur data.toulouse     
    recherche=input("Que voulez-vous rechercher ? Je suis a votre service (enfin data.toulouse pas moi )\n")

    q = urllib.parse.urlencode ({ 'q' : recherche})
#Récuperation de l'url de la base de données recherchée
    url = 'https://data.toulouse-metropole.fr/api/datasets/1.0/search/?%s' %q
#Ouverture de l'url
    search = urllib.request.urlopen(url)
#Chargement de la base de données dans un objet Json
    json = simplejson.loads(search.read())
#Récuperation du nombre des datasets extraits
    nbset=json['nhits']
    
    listeset=[]

    nbenr=[]
#Récuperation du titre de chaque dataset    
    for i in range (0,nbset):
        listeset.append(json['datasets'][i]['metas']['title'])
#Récuperation du nombre d'enregistrements dans chaque dataset    
    for i in range (0,nbset):
        nbenr.append(json['datasets'][i]['metas']['records_count'])
#Si on trouve aucun dataset relatif au mot clé recherché 
    if nbset==0:
        print(" Je ne trouve rien ! Voulez-vous essayer avec un autre mot clé ?")
        rep=input("repondez par oui ou non")
#Refaire la recherche(la boucle globale) dés le debut ou sortir du programme
        break
    else:
        rep='non'

        print("J'ai trouvé " + str(nbset)+ " datasets : \n")
#Affichage des métadonnées de chaque dataset à savoir : sa description, le nombre de ses enregistrements et son index dans la liste
        for i in range (0, len(listeset)):
            print(str(i)+'- '+listeset[i]+ ' avec ' + str(nbenr[i]) + ' enregistrements' +'\n')
            print("\t"+ json['datasets'][i]['metas']['description'] +"\n")
        print("Voulez-vous télécharger les données ?")
#Saisie des index des datasets voulus , "all" pour tout les datasets et "no" sinon 
        tele=input("Donner le chiffre associé a ce que vous voulez télécharger : de 0 à "+ str( nbset ) + ". Ecrivez 'all' pour tout télécharger et 'no' pour ne rien télécharger \n")

        if tele=='no':
            print("OK, tant pis ! ciao")
#Téléchargement de tous les datasets 
        elif tele=='all':
            for i in range (0,nbset):
                q=json['datasets'][int(i)]['datasetid']
                url="https://data.toulouse-metropole.fr/api/records/1.0/download/?dataset=%s" %q
                response = requests.get(url)

                with open('%s.csv' %q, 'wb') as f:
                    f.write(response.content)
#Téléchargement d'un dataset précis           
        else :
            avecq=input("voulais vous filtrer les recherches ? Repondez par oui ou non\n")
            if avecq=='oui':
#Filtre du dataset par un mot clé               
                req=input("quel est votre filtre?\n")
                q=json['datasets'][int(tele)]['datasetid']
                url="https://data.toulouse-metropole.fr/api/records/1.0/download/?dataset="+q+"&q=%s" %req
                url2="https://data.toulouse-metropole.fr/api/records/1.0/search/?dataset="+q+"&q=%s" %req
#Enregistrement du fichier sur .json et .csv
                response = requests.get(url)
                search1 = urllib.request.urlopen(url2)

                json1 = simplejson.loads(search1.read())

                nbset1=json1['nhits']
                print("votre fichier filtré contient "+ str(nbset1) +" enregistrements")
                rep_tel=input("Voulez-vous le telecharger ?\n")
                if rep_tel=='oui':
                    nomfichier=q+"avec-filtre-"+req
                    with open('%s.csv' %nomfichier, 'wb') as f:
                        f.write(response.content)

                

                
            q=json['datasets'][int(tele)]['datasetid']
            url="https://data.toulouse-metropole.fr/api/records/1.0/download/?dataset=%s" %q
            response = requests.get(url)
            with open('%s.csv' %q, 'wb') as f:
                f.write(response.content)

        

            

    
