
# Groupe 3.
# V2.0.2
# récupération de l'état et de la sous catégorie
# modifications pour respecter la charte

from bs4 import BeautifulSoup
import urllib.request
import urllib.parse
import re
import json
import time

# Mise en place d'un timer


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

# Entre : la description de l'objet issue de l'annonce.
# Objectif : suppression des \n\t.
# Sortie : une description nette et lisible.

def cleanString(string):
    if string is not None:
        tmp = string.replace('\n', '')
        return (tmp.replace('\t', '')).strip()


# fonction qui attribut un etat a l'objet

# Entre : la description de l'objet issue de l'annonce.
# Objectif : associé a chaque objet un état.
# Sortie : l'état de l'objet vendu.

def etat(description):
    good = 0

    bad = 0

    normal = 0

    condition = 'Etat moyen'

    description = description.lower()

    condition_dictionary = {}

    condition_dictionary["tbe"] = "Bon etat"

    condition_dictionary["bon etat"] = "Bon etat"

    condition_dictionary["bonne etat"] = "Bon etat"

    condition_dictionary["be"] = "Bon etat"

    condition_dictionary["neuf"] = "Bon etat"

    condition_dictionary["excelent etat"] = "Bon etat"

    condition_dictionary["nef"] = "Bon etat"

    condition_dictionary["peu utilise"] = "Bon etat"

    condition_dictionary["parfait etat"] = "Bon etat"

    condition_dictionary["sous emballage"] = "Bon etat"

    condition_dictionary["sous blister"] = "Bon etat"

    condition_dictionary["servie"] = "Bon etat"

    condition_dictionary["servi"] = "Bon etat"

    condition_dictionary["etat moyen"] = "etat moyen"

    condition_dictionary["global moyen"] = "etat moyen"

    condition_dictionary["produit moyen"] = "etat moyen"

    condition_dictionary["pour bricoleur"] = "mauvais etat"

    condition_dictionary["pour recuperation"] = "mauvais etat"

    condition_dictionary["Panne"] = "mauvais etat"

    condition_dictionary["mauvais etat"] = "mauvais etat"

    condition_dictionary["hs"] = "mauvais etat"

    condition_dictionary["cassé"] = "mauvais etat"

    for regex in condition_dictionary.keys():
        if re.search(regex, str(description)):

            if condition_dictionary[regex] == 'Bon etat':

                good = good + 1

            if condition_dictionary[regex] == 'etat moyen':

                normal = normal + 1

            if condition_dictionary[regex] == 'mauvais etat':

                bad = bad + 1

    if good <= normal:

        if normal < bad:

            condition = 'mauvais etat'

        else:

            condition = 'etat moyen'

    else:

        if good < bad:

            condition = 'mauvais etat'

        else:

            condition = 'Bon etat'

    return condition


# début du timer

timer = Timer()
timer.start()

# declaration et initialisation des variables

ListeUrl = []
Json = []

ListeCat = ['linge_de_maison',
            'velos',
            'arts_de_la_table',
            'autres',
            'electromenager',
            'bricolage',
            'ameublement',
            'jardinage',
            'decoration',
            'vetements']

subcategory = ['armoire',
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


# recuperation de 3 * 35 url d annonces par categorie
for Cat in ListeCat:
    for i in range(0, 3):
        url = 'https://www.leboncoin.fr/%s/?o=%d&location=Toulouse' % (Cat, i)
        search = urllib.request.urlopen(url)
        soup = BeautifulSoup(search, 'html.parser')
        regex = '//www.leboncoin.fr/%s/[0-9]+' % Cat
        for link in soup.find_all('a'):
            if re.search(regex, str(link.get('href'))):
                ListeUrl.append(link.get('href'))
# mise en place d'un dict contenant les informations qu'on recupere de chaque annonce               
for url in ListeUrl:
    information_dictionary = {}

    search = urllib.request.urlopen('https:'+url)

    soup = BeautifulSoup(search, 'html.parser')

    search_price = soup.find("h2", {"itemprop": "price"})

    if search_price is None:

        information_dictionary['prix'] = 'Null'

    else:

        information_dictionary['prix'] = search_price['content']

    search_desc = soup.find("p", {"itemprop": "description"})
    information_dictionary['Description'] = cleanString(search_desc.get_text())

    search_title = soup.find("h1", {"itemprop": "name"})
    information_dictionary['Titre'] = cleanString(search_title.get_text())

    search_date = soup.find("p", {"itemprop": "availabilityStarts"})
    information_dictionary['Date'] = search_date['content']

    search_add = soup.find("span", {"itemprop": "address"})
    information_dictionary['Address'] = cleanString(search_add.get_text())

    information_dictionary['Etat'] = etat(information_dictionary['Description'])

    for regex in subcategory:
        if ((re.search(regex, information_dictionary['Description'])) or (re.search(regex, information_dictionary['Titre']))):
            information_dictionary['Sous Catégorie'] = regex

    search_url = soup.find("span", {"class": "lazyload"})
    if search_url is not None:
        information_dictionary['URL Image'] = search_url['data-imgsrc']
    else:
        information_dictionary['URL Image'] = 'Null'

    for cat in ListeCat:
        if re.search(cat, url):
            information_dictionary["Catégorie"] = cat

    Json.append(information_dictionary)

# Ecriture du fichier Json

with open('data.json', 'w', encoding='utf8') as json_file:
    json.dump(Json, json_file, ensure_ascii=False, indent=2)

timer.stop()
print('Total en seconde :', timer.interval)
