#toeveogen alle library's
import asyncio
import tkinter
from tkinter import *
from PIL import ImageTk, Image
from datetime import datetime
import random
import csv
import psycopg2
import requests
import math
#einde toevoegen librarys
api_key = "c1ea90dc353396b8ef9573319e598c85"# Api key string, word gebruikt voor toegang tot wheater API
connection_string = "host='localhost' dbname='stationzuilfinal' user='postgres' password='kaas'"# string voor connecten emt database

stationslijst = ['Arnhem', 'Almere', 'Oss'] #lijst met de 3 gekozen stations

root = Tk()# initialiseert tinker(GUI)
root.configure(bg="#003082")# Zet de achtergrond van de GUI
def get_temprature(stad):
    """"
    Deze code maakt connectie met de wheaterAPI, deze code vraagt om een stad, en returned de tempretatuur
    in de doorgegeven stad.
    """
    response = requests.get("http://api.openweathermap.org/geo/1.0/direct?q={},NL&limit=1&appid={}".format(stad, api_key)) # haalt de gegevens op van de wheater API
    lat = response.json()[0]['lat'] # pakt de Latitude uit de Json response geeft de waarde aan de variable Lat
    lon = response.json()[0]['lon'] # pakt de Longitude uit de Json response geeft de waarde aan de variable Lon

    response =  requests.get("https://api.openweathermap.org/data/2.5/weather?lat={}&lon={}&appid={}".format(lat, lon, api_key))
    #Haalt de Temperatuur op uit de Wheater Api gebruikt daarbij de eerder verkregen lat en lon
    temperature = response.json()["main"]["temp"] -273.15 #geeft de temperatuur in celsius
    temperature = math.floor(temperature)# rond de temperatuur af
    return temperature # returned de temperatuur
def get_time():
    """
    Deze code pakt de huidige tijd en datum, zet het in een lijst.
    Deze code returned daarna deze lijst.
    """
    secconds = datetime.now().second# Pakt huidige seconde
    minute = datetime.now().minute # pakt huidig minuut
    hour = datetime.now().hour# pakt huidig uur
    tijd_string = str(hour) + ":" + str(minute) + ":" + str(secconds)# plakt uur, minuut en seconde aan elkaar

    month = datetime.now().month# pakt huidige maand
    date = datetime.now().day# pakt huidige dag
    year = datetime.now().year# pakt huidig jaar
    datum_string = str(year) + "-" + str(month) + "-" + str(date)# plakt jaar, maand en dag aan elkaar
    lijst = [tijd_string, datum_string]# zet de tijd en datum in een lijst
    return lijst # returned de lijst

def randomstation():
    """"
    kiest een random station uit de lijst
    returned:
    een random station uit de lijst
    """
    i = 0
    while i == 0:
        stations = ['Arnhem','Almere', 'Oss']
        station = stations[random.randrange(0,3)]# kiest een random station uit de lijst stations
        i = 1
    return station # returned dit station
station = randomstation()# geeft de waarde van het random station aan de globale waarde station.


def standaarvragen(naam, bericht):
    """"
    Code vraagt om een naam, en bericht, kijkt als het bericht niet te lang is. en als de ingevulde naam leeg is
    word de naam naar anoniem gezet, als dit klopt word de tijd toegevoegd en word het naar een csv bestand
    geschreven
    """
    lijst = []

    if naam == "": # als er niks bij naam ingevuld is word de naam naar anoniem gezet
        naam = "anoniem"
    if len(bericht) > 140: # als het bericht langer dan 140 characters is word er opnieuw om de gegevens gevraagd
        gebruikersvragen()
    else: # als het bericht niet langer is, word de gebruiker naar een scherm gestuurd waar je ziet dat het succesvol gelukt is
        bericht_achtergelaten()

    tijd = get_time() # haalt de tijd op uit de functie "get_time" en geeft dit aan de waarde tijd
    gebruiker_gegevens = [naam, bericht]
    gebruiker_gegevens.append(tijd[0])
    gebruiker_gegevens.append(tijd[1])
    gebruiker_gegevens.append(station)
    # gegevens zijn toegevoeg aan een lijst
    with open("kaas.csv") as reader:# opent de file, en leest alles wat in het bestand staat en voegt dat toe aan een lijst
        read = csv.reader(reader, delimiter=',')
        for lines in read:
            lijst.append(lines)

    lijst.append(gebruiker_gegevens)# voegt de gegevens toe aan de lijst

    print(lijst)
    with open("kaas.csv", "w", newline='') as f:# write alles inclusief de nieuwe data terug naar het bestand
        write = csv.writer(f)
        write.writerows(lijst)


def moderator_start(naam, e_mail, keuring):
    """"
    vraagt op de naam, e-mail, en als het goed of afgekeurd is.
    deze gegevens worden daarna naar een database geschreven
    """
    lijst = []
    with open("kaas.csv") as reader:# leest alle informatie uit het csv bestand
        read = csv.reader(reader, delimiter=',')
        for lines in read:
            lijst.append(lines)
    lijst_leeg = []
    if lijst == lijst_leeg:
        moderator_eind_scherm()
    if keuring != "goedgekeurd" and keuring != "afgekeurd":
        moderator_scherm(lijst[0][0], lijst[0][1], naam, e_mail)

    if keuring == "goedgekeurd" or keuring == "afgekeurd":# als het bericht goed of afgekeurd is word onderstaande code uitgevoerd
        print("kaas")
        print(lijst[0][1])
        moderator_tijd = get_time()# pakt de tijd uit de functie "Get_Time()"
        tijd_string = moderator_tijd[0] # voegt de waardes toe aan een lijst
        datum_string = moderator_tijd[1] # Voegt de waardes toe aan een lijst
        conn = psycopg2.connect(connection_string)  # Maakt een conectie met de database
        cursor = conn.cursor() # plaats de cursor
        query = """INSERT INTO keuring ( goed_afgekeurd, datum, tijd) 
                           VALUES (%s, %s, %s);""" # Query vor het writen van "goed_afgekeurd", "datum", "tijd" naar de tabel keuring
        query1 = """INSERT INTO review (  datum, tijd, naam, bericht, station )
                           VALUES ( %s, %s, %s, %s, %s);""" # Query voor het writen van datum, tijd,naam,bericht,station naar de tabel review
        query2 = """INSERT INTO moderator ( naam, e_mail_adres)
                           VALUES (%s, %s);"""# query voor het writen van naam, e_mail_adres naar de tabel moderator
        data = (keuring, datum_string, tijd_string)# vult de waardes in op de placeholders
        data1 = (lijst[0][3], lijst[0][2], lijst[0][0], lijst[0][1], lijst[0][4])# vult de waardes in op de placeholders
        data2 = (naam, e_mail)# vult de waardes in op de placeholders
        cursor.execute(query, data)# writen van de data en de queries naar de database
        cursor.execute(query1, data1)# writen van de data en de queries naar de database
        cursor.execute(query2, data2)# writen van de data en de queries naar de database
        conn.commit()# commit de executes
        conn.close()# sluit de database connectie
        lijst1 = lijst[1:]# haalt de eerste lijn uit de lijst
        with open("kaas.csv", "w", newline='') as f:# write de lijst zonder de eerste waarde terug naar het csv bestand
            write = csv.writer(f)
            write.writerows(lijst1)
        moderator_start(naam, e_mail,"")

def root_clear():
    """"
    Maakt het Gui scherm leeg
    """
    for widget in root.winfo_children():
        widget.destroy()


def bericht_achtergelaten():
    """"
    laat de gebruiker weten dat het bericht succesvol verzonden is

    """
    root_clear()
    frame = Frame(master=root, # create een frame
                   background="",
                   height=300)
    label = Label(master=frame,# create een label
                  text="NS Station /station/",
                  height=2,
                  background='#FFC917',
                  font=("helvetica",12,"bold"),
                  foreground='#003082')
    label.pack()# packed de label
    frame.pack(ipadx=300, ipady=8, pady=(0, 70)) # packed het frame

    frame1 = Frame(master=root,# create een frame
                   background= '#FFC917',
                   height=400)

    label1 = Label(master=frame1,# create een label
                   text="Bericht succesvol verzonden!",
                   background='white',
                   font=("helvetica",16, 'bold'),
                   foreground='#003082',
                   padx=20)
    label1.grid(pady=(0,10), column=0, row=0, columnspan=2) # packed de label met een grid
    label2 = Label(master=frame1,# create een label
                   text="Het bericht is succesvol verzonden,\nen zal binnenkort beoordeeld worden",
                   background='#FFC917',
                   font=("helvetica",12, 'bold'),
                   foreground='#003082',
                   padx=20)
    label2.grid(pady=(0,10), column=0, row=1, columnspan=2)# packed de label met een grid
    frame1.pack(pady=(0, 70))# create een frame



def gebruikersvragen():
    """"
       Dit is het scherm waar mensen hun bericht en naam achter kunnen laten
    als mensen op de knop drukt worden deze waarde doorverwezen naar de functie standaarvragen() daar word het
    naar een csv bestand geschreven

    """
    root_clear()
    frame = Frame(master=root,
                   background="#FFC917",
                   height=300)
    label = Label(master=frame,# create een label
                  text="NS Station: {}".format(station),
                  height=2,
                  background='#FFC917',
                  font=("helvetica",12,"bold"),
                  foreground='#003082')
    label.pack() # packed de label
    frame.pack(ipadx=300, ipady=8, pady=(0, 70))# packed het frame


    frame1 = Frame(master=root,# create een frame
                   background= '#FFC917',
                   height=400)

    label1 = Label(master=frame1,# create een label
                   text="Laat hier uw opmerking achter!",
                   background='white',
                   font=("helvetica",16, 'bold'),
                   foreground='#003082',
                   padx=20)
    label1.grid(pady=(0,10), column=0, row=0, columnspan=2) # packed de label met een grid
    label2 = Label(master=frame1,# create een label
                   text="Naam:",
                   foreground='#003082',
                   font=("Helvetica", 12, 'bold'),
                   background='#FFC917')
    label2.grid(padx=20, column=0, row= 1, sticky="w")# packed de label met een grid
    label3 = Label(master=frame1,# create een label
                   text="Bericht:",
                   foreground='#003082',
                   font=("Helvetica", 12, 'bold'),
                   background='#FFC917')
    label3.grid(padx=20, pady=20, row=2, column=0, sticky="w")# packed de label met een grid

    entry = Entry(master=frame1) # create een entry vak waar gebruiker gegevens in kunnen vullen
    entry.grid(column=1, row=1) #packed de entry met een grid

    entry1 = Entry(master=frame1)# create een entry vak waar gebruiker gegevens in kunnen vullen
    entry1.grid(column=1, row=2) # packed de entry met een grid

    button = Button(master=frame1, # create een button waar mensen op kunnen klikken, als deze button ingedrrukt word
                    #de functie "standaardvragen()gestart met de gegevens ingevuld in de entry's"
                    text="verzenden",
                    background="#003082",
                    foreground="#FFC917",
                    command=lambda: standaarvragen(entry.get(), entry1.get()))
    button.grid(row=3, column=0, columnspan=2, pady=(0, 20))# packed de button met een grid

    frame1.pack(pady=(0, 70)) #packed de frame
    root.mainloop()

def moderator_scherm_inlog():
    """"
    Een scherm waar de moderator kan inloggen door zijn naam en e-mail door te geven

    """
    root_clear()
    frame = Frame(master=root,
                   background="#FFC917",
                   height=300)
    label = Label(master=frame,# create een label
                  text="NS Station /station/",
                  height=2,
                  background='#FFC917',
                  font=("helvetica",12,"bold"),
                  foreground='#003082')
    label.pack()# packed de label met een grid
    frame.pack(ipadx=300, ipady=8, pady=(0, 70)) # packed de frame
    frame1 = Frame(master=root,# create een label
                   background= '#FFC917',
                   height=400)

    label1 = Label(master=frame1,# create een label
                   text="Moderator inlog",
                   background='white',
                   font=("helvetica",16, 'bold'),
                   foreground='#003082',
                   padx=20)
    label1.grid(pady=(0,10), column=0, row=0, columnspan=2)# packed de label met een grid
    label2 = Label(master=frame1,# create een label
                   text="Naam:",
                   foreground='#003082',
                   font=("Helvetica", 12, 'bold'),
                   background='#FFC917')
    label2.grid(padx=20, column=0, row= 1, sticky="w")# packed de label met een grid
    label3 = Label(master=frame1,# create een label
                   text="E-mail",
                   foreground='#003082',
                   font=("Helvetica", 12, 'bold'),
                   background='#FFC917')
    label3.grid(padx=20, pady=20, row=2, column=0, sticky="w")# packed de label met een grid

    entry = Entry(master=frame1) # create een Entry
    entry.grid(column=1, row=1) # packed een entry met een grid

    entry1 = Entry(master=frame1)# create een Entry
    entry1.grid(column=1, row=2) # packed een enrty met een grid

    button = Button(master=frame1,# create een button start de code moderator_Start
                    text="verzenden",
                    background="#003082",
                    foreground="#FFC917",
                    command=lambda: moderator_start(entry.get(), entry1.get(), "leeg"))
    button.grid(row=3, column=0, columnspan=2, pady=(0, 20), padx=200) # packed de button met een grid


    frame1.pack(pady=(0, 70)) # packed de frame
def moderator_scherm(naam, bericht, e_mail,naam_mod):
    """"
    een scherm waar een ingelogde moderator berichten kan goed/afkeuren
    """
    root_clear()
    frame = Frame(master=root,# create een label
                  background="#FFC917",
                  height=300)
    label = Label(master=frame,
                  text="NS Station /station/",
                  height=2,
                  background='#FFC917',
                  font=("helvetica", 12, "bold"),
                  foreground='#003082')
    label.pack() # packed de label met een grid
    frame.pack(ipadx=300, ipady=8, pady=(0, 70))# packed een frame


    frame1 = Frame(master=root,# create een frame
                   background= '#FFC917',
                   height=400)

    label1 = Label(master=frame1,# create een label
                   text="Moderator beoordeling",
                   background='white',
                   font=("helvetica",16, 'bold'),
                   foreground='#003082',
                   padx=20)
    label1.grid(pady=(0,10), column=0, row=0, columnspan=2)# packed de label met een grid
    label2 = Label(master=frame1,# create een label
                   text="Naam:",
                   foreground='#003082',
                   font=("Helvetica", 12, 'bold'),
                   background='#FFC917')
    label2.grid(padx=20, column=0, row= 1, sticky="w")# packed de label met een grid
    label3 = Label(master=frame1,# create een label
                   text="bericht",
                   foreground='#003082',
                   font=("Helvetica", 12, 'bold'),
                   background='#FFC917')
    label3.grid(padx=20, pady=20, row=2, column=0, sticky="w")# packed de label met een grid

    label4 = Label(master=frame1,# create een label
                   text=naam,
                   foreground='#003082',
                   font=("Helvetica", 12, 'bold'),
                   background='#FFC917')
    label4.grid(column=1, row=1)# packed de label met een grid

    label5 = Label(master=frame1,# create een label
                   text=bericht,
                   foreground='#003082',
                   font=("Helvetica", 12, 'bold'),
                   background='#FFC917',
                   wraplength=250)
    label5.grid(column=1, row=2)# packed de label met een grid

    button = Button(master=frame1, # create een button, start de code moderator_start
                    text="Goedkeuren",
                    background="#003082",
                    foreground="#FFC917",
                    command=lambda: moderator_start(naam_mod, e_mail, "goedgekeurd"))
    button.grid(row=3, column=0, pady=(0, 20))
    button1 = Button(master=frame1, # create een button, start de code moderator_start
                    text="Afkeuren",
                    background="#003082",
                    foreground="#FFC917",
                    command=lambda: moderator_start(naam_mod, e_mail, "afgekeurd"))

    button1.grid(row=3, column=1, pady=(0, 20) ) # packed de button met een grid

    frame1.pack(pady=(0, 70)) # packed het frame

def moderator_eind_scherm():
    """"
    geeft door aan de moderator dat er geen reviews meer zijn om te beoordelen

    """
    root_clear()
    frame = Frame(master=root,# create een frame
                   background="#FFC917",
                   height=300)
    label = Label(master=frame,# create een label
                  text="NS Station /station/",
                  height=2,
                  background='#FFC917',
                  font=("helvetica",12,"bold"),
                  foreground='#003082')
    label.grid(pady=(0,10), column=0, row=0, columnspan=2)# packed de label met een grid
    frame.grid(pady=(0,10), column=0, row=0, columnspan=2)# packed de frame met een grid

    frame1 = Frame(master=root,# create een frame
                   background= '#FFC917',
                   height=400)

    label1 = Label(master=frame1,# create een label
                   text="moderator",
                   background='white',
                   font=("helvetica",16, 'bold'),
                   foreground='#003082',
                   padx=20)
    label1.grid(pady=(0,10), column=0, row=0, columnspan=2)
    label2 = Label(master=frame1,# create een label
                   text="Er zijn berichten meer om te beoordelen",
                   background='#FFC917',
                   font=("helvetica",12, 'bold'),
                   foreground='#003082',
                   padx=20)
    label2.grid(pady=(0,10), column=0, row=1, columnspan=2)# packed de label met een grid
    frame1.grid(pady=(0, 10), column=0, row=0, columnspan=2)  # packed de frame met een grid

def station_scherm_begin():
    """"
    Een scherm waar de gebruiker kan kiezen op welk station de stationscherm staat
    """
    root_clear()
    frame = Frame(master=root,# create een frame
                   background="#FFC917",
                   height=300)
    label = Label(master=frame,# create een label
                  text="Station keuze",
                  height=2,
                  background='#FFC917',
                  font=("helvetica",12,"bold"),
                  foreground='#003082')
    label.pack()# packed een label
    frame.pack(ipadx=300, ipady=8, pady=(0, 70))# packed een frame


    frame1 = Frame(master=root,# create een frame
                   background= '#FFC917',
                   height=400)

    label1 = Label(master=frame1,# create een label
                   text="Selecteer een station!",
                   background='white',
                   font=("helvetica",16, 'bold'),
                   foreground='#003082',
                   padx=20)
    label1.grid(pady=(0,10), column=0, row=0, columnspan=2)# packed een label met een grid
    label2 = Label(master=frame1,# create een label
                   text="Station:",
                   foreground='#003082',
                   font=("Helvetica", 12, 'bold'),
                   background='#FFC917')
    label2.grid(padx=10, column=0, row= 1, sticky="w")# packed een label met een grid

    placeholder = tkinter.StringVar()# create een dropdown menu
    placeholder.set("kies een station")
    option = tkinter.OptionMenu(frame1, placeholder, *stationslijst)
    option.grid(row = 1, column=1)

    button = Button(master=frame1,# create een button en start de code stationscherm()
                    text="verzenden",
                    background="#003082",
                    foreground="#FFC917",
                    command=lambda: station_scherm(placeholder.get()))
    button.grid(row=3, column=0, columnspan=2, pady=(0, 20))# packed de button met een grid


    frame1.pack(pady=(0, 70))# packed het frame

    root.mainloop()

def station_scherm(station):
    """"
    Deze functie is het stationscherm, hier worden de laatste 5 berichten uit de database gehaald, en word op
    een stationscherm laten zien.


    """
    if station == "kies een station":
        station_scherm_begin()
    temperatuur = get_temprature(station) # krijgt de temperatuur van het gekozen station en geeft deze waarde aan temperatuur
    naamlijst = []
    berichtlijst = []
    stationlijst = []
    conn = psycopg2.connect(connection_string)  # maakt een connectie met de database
    cursor = conn.cursor()# plaatst de cursor
    query = """select bericht, naam , review.tijd , review.datum, station
                from keuring, review
                where keuring.keuring_id = review.keuring_id
                and keuring.goed_afgekeurd = 'goedgekeurd'
                ORDER BY review.datum, review.tijd Desc
                limit 5;"""  # pakt de laatste 5 goedgekeurde review uit de database
    cursor.execute(query)# execute de query
    records = cursor.fetchall()  # haalt de gegevens uit de database
    conn.close()# sluit de connectie met de database
    for record in records:# voegt alle gegevens toe aan een lijsten
        naamlijst.append(record[1])
        berichtlijst.append(record[0])
        stationlijst.append(record[4])


    # hieronder worden alle faciliteiten images geladen en geresized
    image = Image.open("img_lift.png")
    resize_image = image.resize((25, 25))
    img_lift = ImageTk.PhotoImage(resize_image)

    image1 = Image.open("img_pr.png")
    resize_image1 = image1.resize((25, 25))
    img_pr = ImageTk.PhotoImage(resize_image1)

    image2 = Image.open("img_toilet.png")
    resize_image2 = image2.resize((25, 25))
    img_toilet = ImageTk.PhotoImage(resize_image2)

    image3 = Image.open("img_ovfiets.png")
    resize_image3 = image3.resize((25, 25))
    img_ovfiets = ImageTk.PhotoImage(resize_image3)
    # einde images


    root_clear()
    root.geometry("600x400")


    frame = Frame(master=root,# create een frame
                  background="#FFC917",
                  height=300)
    label = Label(master=frame,# create een label
                  text="NS Station: {}".format(station),
                  height=2,
                  background='#FFC917',
                  font=("helvetica", 12, "bold"),
                  foreground='#003082')
    label.pack()# packed de label
    frame.pack(ipadx=300, ipady=8, pady=(0, 0))# packed het frame


    frame2 = Frame(master=root,# create een frame
                  background="white",
                  height=300)
    label2 = Label(master=frame2,# create een label
                  text="Temperatuur: {}". format(temperatuur),
                  height=2,
                  background='white',
                  font=("helvetica", 12, "bold"),
                  foreground='#003082')
    label2.pack()# packed de label
    frame2.pack(ipadx=300, ipady=8)# packed het frame

    frame1 = Frame(master=root,# create een frame
                   height=400,
                   width=20,
                   background="#003082",
                   )
    for frame in range(len(stationlijst)):# een loop die zo vaak runned als de lijst stationlijst lang is
        #onderstaande code kijkt welke faciliteiten bij het station zitten
        if stationlijst[frame] == "Arnhem":
            picture1 = img_ovfiets
            picture2 = img_toilet
        elif stationlijst[frame] == "Almere":
            picture1 = img_lift
            picture2 = img_pr
        elif stationlijst[frame] == "Oss":
            picture1 = img_lift
            picture2 = img_pr
        #einde faciliteiten
        coolframe = Frame(master= frame1,# create een frame
                          width= 20)
        label1 = Label(master=coolframe,# create een label
                       text=naamlijst[frame],
                       background='white',
                       font=("helvetica", 12, 'bold'),
                       foreground='#003082',
                       width=10,)
        label1.grid(sticky= "ew", pady=(10,0))# create een label met een grid
        label2 = Label(master=coolframe,# create een label
                       text="Station: {}".format(stationlijst[frame]),
                       foreground='#003082',
                       font=("Helvetica", 8, 'bold'),
                       background='grey',
                       width=10)
        label2.grid(sticky= "ew")# packed de label met een grid
        label3 = Label(master=coolframe,# create een label
                       text= berichtlijst[frame],
                       foreground='#003082',
                       font=("Helvetica", 7),
                       background='#FFC917',
                       wraplength=100,
                       width=10)
        label3.grid(sticky="ews")# packed een label met een grid
        label4 = Label(master=coolframe,# create een label
                       text= "Faciliteiten:",
                       foreground="#003082",
                       font=("Helvetica", 6, 'bold'),
                       background="#FFC917",
                       wraplength=100,
                       width=10)
        #onderstaande code voegt de plaatjes onder de faciliteiten toe
        label4.grid(sticky="ew", row= 4,column= 0,columnspan=2)
        label7 = Label(master=coolframe, background="#FFC917")
        label7.grid(row=5, sticky="nesw")
        label5 = Label(master=coolframe, image=picture1, background= "#FFC917")
        label5.image = picture1
        label5.grid(row=5, column=0, sticky="w", padx=25)
        label6 = Label(master=coolframe, image= picture2, background="#FFC917")
        label6.image = picture2
        label6.grid(row=5 , column=0, sticky="w")


        coolframe.grid(sticky="w",column=frame, row=0, padx=5,pady=(20,0))# packed het frame met een grid




    frame1.pack()# packed het frame


def startscherm():
    """"
    dit is het startscherm, hier kunnen gebruikers kiezen wat ze willen doen, ze kunnen kiezen uit,
    stationscherm, moderator en bericht achterlaten

    """
    #create de achtergrond
    blue_frame = tkinter.Frame(bd=0, highlightthickness=0, background='#003082')
    yellow_frame = tkinter.Frame(bd=0, highlightthickness=0, background='#FFC917')
    yellow_frame1 = tkinter.Frame(bd=0, highlightthickness=0, background='#FFC917')
    yellow_frame.place(x=0, y=0, relwidth=1, relheight=.25, anchor="nw")
    blue_frame.place(x=0, rely=.25, relwidth=1, relheight=.75, anchor="nw")
    yellow_frame1.place(relx=0.19, rely=0.4, relwidth=0.62, relheight=.5, anchor="nw")
    #einde achtergrond
    label = Label(master=root,# create een label
                  text="NS Startscherm",
                  height=2,
                  background='#FFC917',
                  font=("helvetica",12,"bold"),
                  foreground='#003082')
    label.pack(side=TOP, padx=20, pady=40) #packed de label
    label1 = Label(master=root,# create de label
                   text="Kies 1 van onderstaande opties:",
                   background='white',
                   font=("helvetica",12, 'bold'),
                   foreground='#003082')
    label1.pack(ipady=10, ipadx=60)#packed de label

    button1 = Button(master=root,# create de button die de code Stationscherm start
                     text="Stationscherm",
                     background='#003082',
                     foreground='white',
                     command=station_scherm_begin
                     )
    button1.pack(ipadx=20, ipady=10,pady=3) # packed de button

    button2 = Button(master=root,# create de button die de code moderator_scherm_inlog() start
                     text="Moderator",
                     background='#003082',
                     foreground='white',
                     command=moderator_scherm_inlog
                     )
    button2.pack(ipadx=20, ipady=10,pady=3)# packed de button

    button3 = Button(master=root,# # create de button die de code gebruikervragen() start
                     text="Bericht achterlaten",
                     background='#003082',
                     foreground='white',
                     command= gebruikersvragen)
    button3.pack(ipadx=20, ipady=10,pady= 3)# Packed de button
    root.geometry("600x400")
    root.mainloop()
startscherm()
