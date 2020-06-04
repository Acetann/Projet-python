#!/usr/bin/env python
# -*- coding: utf-8 -*-

from flask import Flask, render_template
import requests, json
import random

app = Flask(__name__)


@app.route("/")
def home():
    Key = "77153ff2-4e4c-4b27-bd27-51151cfd65cd"

    Objet = random.randint(1, 20)

    url = "https://api.cdiscount.com/OpenApi/json/Search"
    params = {
        "ApiKey": Key,
        "SearchRequest": {
            "Keyword": "tv",
            "Pagination": {
                "ItemsPerPage": Objet,
                "PageNumber": 1
            },
            "Filters": {
                "Price": {
                    "Min": 0,
                    "Max": 0
                },
                "Navigation": "tv",
                "IncludeMarketPlace": "false"
            }
        }
    }

    r = requests.post(url, data=json.dumps(params))
    var = (r.json()['Products'][0]['Name'])
    vari = (r.json()['Products'][0]['BestOffer']['SalePrice'])

    return render_template("hello.html", Bolosse=var, Tagueule=vari)


if __name__ == "__main__":
    app.run()
