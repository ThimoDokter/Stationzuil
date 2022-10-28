import time
import random
import csv
import psycopg2


def gebruikers_vragen():
    """
    vraagt gegevens van de gebruiker zoals naam en bericht, deze gegevens worden gecontroleerd op lengte en naam.
    returns:
    returned de gegevens in een list deze list is zo opgebouwd [naam, bericht, tijd]
    """
    print("Welkom, Om een review achter te laten vragen wij u graag om een aantal gegevens")

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
station = randomstation()
def csvfilewrite():
    """"
    reads csv file and then adds gebruikers_gegevens and station to file
    :returns
    Nothing
    """
    lijst = []
    gebruiker_gegevens = gebruikers_vragen()
    gebruiker_gegevens.append(station)
    gebruiker_gegevens.append("afwachting")
    with open("kaas.csv") as reader:
        read = csv.reader(reader, delimiter=',')
        for lines in read:
            lijst.append(lines)


    lijst.append(gebruiker_gegevens)

    with open("kaas.csv", "w", newline= '') as f:
        write = csv.writer(f)
        write.writerows(lijst)



def moderator():
    #eerst word er gevraagd om de gegevens van de moderator, zoals naam en e-mailadres
    naam = input("Voer alstublieft uw naam in:")
    e_mail = input("Voer alstublieft uw e-mail in:")
    lijst = []
    with open("kaas.csv") as reader:
        read = csv.reader(reader, delimiter=',')
        for lines in read:
            lijst.append(lines)
    for lines in lijst:
        if lines[4] == "afwachting":
            print("wilt u onderstaande review goedkeuren?(ja of nee)\n naam: {}\n bericht:{}" .format(lines[0], lines[1]))
            input_moderator = input("ja of nee?")
            if input_moderator == "ja":
                print("bericht is goedgekeurd")
                lines[4] = "goedgekeurd"
            elif input_moderator == "nee":
                print("bericht is afgekeurd")
                lines[4] = "afgekeurd"
    print("sorry, er zijn geen reviews meer.")
    with open("kaas.csv", "w", newline= '') as f:
        write = csv.writer(f)
        write.writerows(lijst)





#hieronder is gemaakt om de code te testen
i = 0
while i == 0:
    print("1: Gebruikersvragen")
    print("2: CSVfilewrite")
    print("3: Moderator")
    print("4: Stoppen")
    input1 = int(input("Kies welke code u uit wilt voeren"))
    if input1 == 1:
        gebruikers_vragen()
        print("kaas")
    if input1 == 2:
        csvfilewrite()


    if input1 == 3:
        moderator()

    if input1 == 4:
        i = 1
#hier stop het code testen