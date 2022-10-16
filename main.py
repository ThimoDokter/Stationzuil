import time
import random

print("Welkom, Om een review achter te laten vragen wij u graag om een aantal gegevens")
def gebruikers_vragen():
    """
    vraagt gegevens van de gebruiker zoals naam en bericht, deze gegevens worden gecontroleerd op lengte en naam.
    returns:
    returned de gegevens in een list deze list is zo opgebouwd [naam, bericht, tijd]
    """
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

def randomstation():
    """"
    kiest een random station uit de lijst
    returned:
    een random station uit de lijst
    """
    i = 0
    while i == 0:
        stations = ['Arnhem','Almere', 'Amersfoort', 'Almelo', 'Alkmaar', 'Apeldoorn', 'Assen', 'Amsterdam', 'Boxtel', 'Breda', 'Dordrecht', 'Delft', 'Deventer', 'Enschede', 'Gouda', 'Groningen', 'Haarlem', 'Helmond', 'Hoorn', 'Heerlen', 'Den Bosch', 'Hilversum', 'Leiden', 'Lelystad', 'Leeuwarden', 'Maastricht', 'Nijmegen', 'Oss', 'Roermond', 'Roosendaal', 'Sittard', 'Tilburg', 'Utrecht', 'Venlo', 'Vlissingen', 'Zaandam', 'Zwolle', 'Zutphen']
        station = stations[random.randrange(1,38)]
        print(station)
        i = 1
    return station
randomstation()