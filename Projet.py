from flask import Flask, render_template, request
import requests, json
import random
import datetime
import time

app = Flask(__name__)


@app.route("/", methods=['POST', 'GET'])
def home():
    Key = "77153ff2-4e4c-4b27-bd27-51151cfd65cd"
    Article = random.randint(1, 50)

    Prix = -1
    tentative = []
    tempsdepart = -1
    if request.method == "POST":
        Article = int(request.form["Article"])
        Prix = int(request.form["Prix"])
        tentative = json.loads(request.form["essai"])
        tentative.append(Prix)
        tempsdepart = float(request.form["tempstotal"])
        if tempsdepart == -1:
            tempsdepart = time.time()

    params = {
        "ApiKey": Key,
        "SearchRequest": {
            "Keyword": "food",
            "Pagination": {
                "ItemsPerPage": Article,
                "PageNumber": 1
            },
            "Filters": {
                "Price": {
                    "Min": 0,
                    "Max": 0
                },
                "Navigation": "",
                "IncludeMarketPlace": "false"
            }
        }
    }

    url = "https://api.cdiscount.com/OpenApi/json/Search"

    requête = requests.post(url, data=json.dumps(params))
    nomproduit = (requête.json()['Products'][0]['Name'])
    image = (requête.json()['Products'][0]['MainImageUrl'])
    prixproduit = int(float(requête.json()['Products'][0]['BestOffer']['SalePrice']))

    temps = None
    if request.method == "POST":
        temps = datetime.datetime.now() - datetime.datetime.fromtimestamp(tempsdepart)

    return render_template("hello.html", Nomproduit=nomproduit, Prixproduit=prixproduit, Image=image, Prix=Prix,
                           Article=Article,
                           Essai=tentative, TempsDepart=tempsdepart, Temps=temps)


if __name__ == "__main__":
    app.run()
