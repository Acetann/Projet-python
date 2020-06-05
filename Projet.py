from flask import Flask, render_template, request
import requests, json
import random
import datetime
import time

app = Flask(__name__)


@app.route("/", methods=['POST', 'GET'])
def home():
    # Permet de prendre un objet random de l'API
    Article = random.randint(2, 40)

    # Récupère l'API grâce à la clé fourni
    Key = "77153ff2-4e4c-4b27-bd27-51151cfd65cd"

    # Les paramètres qu'on aura besoin pour afficher les articles et les récupérer
    params = {
        "ApiKey": Key,
        "SearchRequest": {
            "Keyword": "tv",
            "Pagination": {
                "ItemsPerPage": Article,
                "PageNumber": 1
            },
            "Filters": {
                "Price": {
                    "Min": 0,
                    "Max": 1000
                },
                "Navigation": "",
                "IncludeMarketPlace": "false"
            }
        }
    }

    # L'URL du site de CDiscount
    url = "https://api.cdiscount.com/OpenApi/json/Search"

    # On fixe une variable qui sera le prix qu'on tape pour trouver le bon prix
    Prix = 0

    # On crée un dictionnaire qui nous permettra de récupérer les valeurs des tentatives
    tentative = []

    # On initialise le temps de départ avec une valeur négative pour qu'elle soit abérante et non affichable
    tempsdepart = -1

    # Si la méthode est un POST, il va enregister un article et son prix de l'API puis il stockera chaque tentative
    # ainsi que son prix qui s'affichera en front et aussi le temps depuis la première tentative
    if request.method == "POST":
        Article = int(request.form["Article"])
        Prix = int(request.form["Prix"])
        tentative = json.loads(request.form["essai"])
        tentative.append(Prix)
        tempsdepart = float(request.form["tempstotal"])

    # Si le temps de départ est strictement égale à -1 alors le decompte peut se lancer
        if tempsdepart == -1:
            tempsdepart = time.time()

    # Il va récupérer sous format JSON, les paramètres prédéfini dans la variable params pour ensuite potentiellement
    # les afficher si on le souhaite
    requête = requests.post(url, data=json.dumps(params))

    # Il va chercher dans un fichier JSON la valeur 'Products' et ensuite sortir le premier nom de l'article
    nomproduit = (requête.json()['Products'][0]['Name'])

    # Il va chercher dans un fichier JSON la valeur 'Products' et ensuite sortir la première image de l'article
    image = (requête.json()['Products'][0]['MainImageUrl'])

    # Il va chercher dans un fichier JSON la valeur 'Products' puis dans 'BestOffer' et ensuite sortir le premier
    # prix de l'article
    prixproduit = int(float(requête.json()['Products'][0]['BestOffer']['SalePrice']))

    temps = None

    # Si on effectue un POST, le temps s'actualise avec le temps à l'instant T moins le temps de départ ( temps de
    # départ qui démarre à partir du premier prix testé )
    if request.method == "POST":
        temps = datetime.datetime.now() - datetime.datetime.fromtimestamp(tempsdepart)

    # On renvoie le tout vers le fichier .html avec les valeurs qui servira pour le test
    return render_template("index.html", Nomproduit=nomproduit, Prixproduit=prixproduit, Image=image, Prix=Prix,
                           Article=Article,
                           Essai=tentative, TempsDepart=tempsdepart, Temps=temps)


if __name__ == "__main__":
    app.run()
