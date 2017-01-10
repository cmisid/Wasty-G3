from bs4 import BeautifulSoup
import urllib.request
import urllib.parse
import re
import json
import time

#Mise en place d'un timer
class Timer(object):  
    def start(self):  
        if hasattr(self, 'interval'):  
            del self.interval  
        self.start_time = time.time()  
  
    def stop(self):  
        if hasattr(self, 'start_time'):  
            self.interval = time.time() - self.start_time  
            del self.start_time
# Fonction pour nettoyer le texte recupere  
def cleanString(string):
    if string is not None:
        tmp = string.replace('\n', '')
        return (tmp.replace('\t', '')).strip()
#fonction qui attribut un etat a l'objet 
def etat(description):
    bonetat=0

    mauvaisetat=0

    etatmoyen=0
    
    etat='Etat moyen'

    description=description.lower()
    
    mon_dictionnaire = {}

    mon_dictionnaire["tbe"] = "Bon etat"

    mon_dictionnaire["bon etat"] = "Bon etat"

    mon_dictionnaire["bonne etat"] = "Bon etat"

    mon_dictionnaire["be"] = "Bon etat"

    mon_dictionnaire["neuf"] = "Bon etat"

    mon_dictionnaire["excelent etat"] = "Bon etat"

    mon_dictionnaire["nef"] = "Bon etat"

    mon_dictionnaire["peu utilise"] = "Bon etat"

    mon_dictionnaire["parfait etat"] = "Bon etat"

    mon_dictionnaire["sous emballage"] = "Bon etat"

    mon_dictionnaire["sous blister"] = "Bon etat"

    mon_dictionnaire["servie"] = "Bon etat"

    mon_dictionnaire["servi"] = "Bon etat"

    mon_dictionnaire["etat moyen"] = "etat moyen"

    mon_dictionnaire["global moyen"] = "etat moyen"

    mon_dictionnaire["produit moyen"] = "etat moyen"

    mon_dictionnaire["pour bricoleur"] = "mauvais etat"

    mon_dictionnaire["pour recuperation"] = "mauvais etat"

    mon_dictionnaire["Panne"] = "mauvais etat"

    mon_dictionnaire["mauvais etat"] = "mauvais etat"

    mon_dictionnaire["hs"] = "mauvais etat"

    mon_dictionnaire["cassé"] = "mauvais etat"

    for regex in mon_dictionnaire.keys():
        if re.search(regex, str(description)):

            if mon_dictionnaire[regex] == 'Bon etat':

                bonetat=bonetat+1

            if mon_dictionnaire[regex] == 'etat moyen':
              

                etatmoyen=etatmoyen+1

            if mon_dictionnaire[regex] == 'mauvais etat':

                mauvaisetat=mauvaisetat+1
                
    if bonetat<=etatmoyen:

       if etatmoyen<mauvaisetat:

           etat='mauvais etat'
           

       else:

           etat='etat moyen'

    else:

       if bonetat<mauvaisetat:

           etat='mauvais etat'

       else:

           etat='Bon etat'

    return etat
    
    
#début du timer
    
timer = Timer()  
timer.start()

#declaration et initialisation des variables

ListeUrl=[]
Json=[]

ListeCat=['linge_de_maison',
          'velos',
          'arts_de_la_table',
          'autres',
          'electromenager',
          'bricolage',
          'ameublement',
          'jardinage',
          'decoration',
          'vetements']

subcategory=['armoire',
             'buffet',
             'canape',
             'chaise',
             'commode',
             'etagere',
             'fauteuil',
             'fenetre',
             'lit',
             'matelas',
             'porte',
             'pouf',
             'table',
             'table de chevet',
             'tabouret',
             'bougeoire',
             'cadre',
             'coussin',
             'luminaire',
             'miroir',
             'pendule',
             'rideau',
             'tapis',
             'vase',
             'barbecue',
             'echelle',
             'hamac',
             'parasol',
             'aspirateur',
             'climatiseur',
             'congelateur',
             'four',
             'refrigerateur',
             'lave vaisselle',
             'lave linge',
             'ventilateur',
             'poele a bois',
             'ventilateur',
             'balance',
             'batteur',
             'bouilloire',
             'cafetiere',
             'crepiere',
             'fer a repasser',
             'friteuse',
             'gauffrier',
             'grille pain',
             'machine à fondue',
             'micro onde',
             'mixeur',
             'pese personne',
             'plancha',
             'plaque de cuisson',
             'raclette',
             'radiateur',
             'bonnet',
             'chaussure',
             'chemise',
             'couverture',
             'gant',
             'pantalon',
             'pull',
             'serviette',
             'short',
             't shirt',
             'veste',
             'assiette',
             'casserole',
             'couvert',
             'faitout',
             'poele',
             'saladier',
             'theiere',
             'plateau',
             'verre',
             'roller',
             'skateboard',
             'trottinette',
             'velo',
             'baignoire',
             'bocal',
             'boite',
             'bouteille',
             'lavabo',
             'sac',
             'valise',
             'lavabo',
             'tonneau']


#recuperation de 3 * 35 url d annonces par categorie 
for Cat in ListeCat:
    for i in range(0,3):
        url='https://www.leboncoin.fr/%s/?o=%d&location=Toulouse' % (Cat, i)
        search = urllib.request.urlopen(url)
        soup = BeautifulSoup(search, 'html.parser')
        regex='//www.leboncoin.fr/%s/[0-9]+' %Cat
        for link in soup.find_all('a'):
            if re.search(regex,str(link.get('href'))):
                ListeUrl.append(link.get('href'))
#mise en place d'un dict contenant les informations qu'on recupere de chaque annonce                
for url in ListeUrl:
    dicco={}

    search = urllib.request.urlopen('https:'+url)
    
    soup = BeautifulSoup(search, 'html.parser')
    
    RecherchePrix = soup.find("h2", {"itemprop" : "price"})
    
    if RecherchePrix is None:
        
        dicco['prix'] = 'Null'
        
    else:
        
        dicco['prix']=RecherchePrix['content']
        
    RechercheDesc=soup.find("p", {"itemprop" : "description"} )
    dicco['Description']=cleanString(RechercheDesc.get_text())
    
    RechercheTitre=soup.find("h1", {"itemprop" : "name"} )
    dicco['Titre']=cleanString(RechercheTitre.get_text())
    
    RechercheDate = soup.find("p", {"itemprop" : "availabilityStarts"})
    dicco['Date']=RechercheDate['content']
    
    RechercheAdd=soup.find("span", {"itemprop" : "address"} )
    dicco['Address']=cleanString(RechercheAdd.get_text())
    
   
    dicco['Etat']=etat(dicco['Description'])
    
    for regex in subcategory:
        if ((re.search(regex, dicco['Description'])) or (re.search(regex, dicco['Titre']))):
            dicco['Sous Catégorie']=regex

    RechercheUrl=soup.find("span", { "class" : "lazyload" })
    if RechercheUrl is not None:
        dicco['URL Image']=RechercheUrl['data-imgsrc']
    else:
        dicco['URL Image']='Null'

    for cat in ListeCat:
        if re.search(cat,url):
            dicco["Catégorie"]=cat


    Json.append(dicco)

#Ecriture du fichier Json

with open('data.json', 'w', encoding='utf8') as json_file:
    json.dump(Json, json_file, ensure_ascii=False)
    
timer.stop()
print('Total en seconde :', timer.interval)
