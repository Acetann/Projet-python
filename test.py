import requests, json
import random

tentatives = 50
while tentatives > 0:
    var = int(input("Devinez le prix: "))
    if var < Objet:
        appreciation = "Fais un effort c'est plus voyons "
        print(appreciation)
    else:
        appreciation = "Tu le fais exprès ou quoi ? C'est  moins "
        print(appreciation)
    if var == Objet:
        appreciation = "Tu es un vraiment un Colosse !"
        print(appreciation)
        break
    tentatives -= 1
    print(tentatives)

