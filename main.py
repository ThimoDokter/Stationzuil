import time
tm_year = 0

print("Welkom, Om een review achter te laten vragen wij u graag om een aantal gegevens")
#onderstaande functie, vraagt de gegevens van de gebruiker en returnd
def gebruikers_vragen():
    i = 0
    naam = input("Voer alstublieft uw naam in, als uw geen naam in vult word het bericht als anoniem geplaatst")
    if naam == "":
        naam = "anoniem"
        print("uw naam is:", naam)
    else:
        print("uw naam is", naam)
    while i == 0:
        bericht = input("voer altublieft uw bericht in")
        if len(bericht) > 140:
            print("sorry uw bericht is te lang voer alstublieft maximaal 140 characters in.")
            continue
        else:
            print("dit is uw ingevulde bericht:")
            print(bericht)
            i = 1
            break
    tijd = time.asctime()
    print(tijd)
    lijst = [naam, bericht,tijd]
    return lijst
gebruikers_vragen()