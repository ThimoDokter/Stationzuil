import tkinter
from tkinter import *
from datetime import datetime
import random
import csv
import psycopg2

connection_string = "host='localhost' dbname='stationzuilfinal' user='postgres' password='kaas'"



root = Tk()
root.configure(bg="blue")
def get_time():

    secconds = datetime.now().second
    minute = datetime.now().minute
    hour = datetime.now().hour
    tijd_string = str(hour) + ":" + str(minute) + ":" + str(secconds)
    print(tijd_string)

    month = datetime.now().month
    date = datetime.now().day
    year = datetime.now().year
    datum_string = str(year) + "-" + str(month) + "-" + str(date)
    print(datum_string)
    lijst = [tijd_string, datum_string]
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


def standaarvragen(naam, bericht):
    lijst = []

    if naam == "":
        naam = "anoniem"
    if len(bericht) > 140:
        gebruikersvragen()
    else:
        bericht_achtergelaten()

    tijd = get_time()
    gebruiker_gegevens = [naam, bericht]
    gebruiker_gegevens.append(tijd[0])
    gebruiker_gegevens.append(tijd[1])
    gebruiker_gegevens.append(station)

    with open("kaas.csv") as reader:
        read = csv.reader(reader, delimiter=',')
        for lines in read:
            lijst.append(lines)

    lijst.append(gebruiker_gegevens)

    print(lijst)
    with open("kaas.csv", "w", newline='') as f:
        write = csv.writer(f)
        write.writerows(lijst)


def moderator_start(naam, e_mail, keuring):
    moderator_naam = naam
    moderator_e_mail  = e_mail
    lijst = []
    with open("kaas.csv") as reader:
        read = csv.reader(reader, delimiter=',')
        for lines in read:
            lijst.append(lines)
    lijst_leeg = []
    if lijst == lijst_leeg:
        print("lijst is leeg")
        moderator_eind_scherm()
    else:
        lol = moderator_scherm(lijst[0][0], lijst[0][1], naam, e_mail)
        print("kaas")

    if keuring == "goedgekeurd" or keuring == "afgekeurd":

        moderator_tijd = get_time()
        tijd_string = moderator_tijd[0]
        datum_string = moderator_tijd[1]
        conn = psycopg2.connect(connection_string)  # get a connection with the database
        cursor = conn.cursor()
        query = """INSERT INTO keuring ( goed_afgekeurd, datum, tijd)
                           VALUES (%s, %s, %s);"""
        query1 = """INSERT INTO review (  datum, tijd, naam, bericht, station )
                           VALUES ( %s, %s, %s, %s, %s);"""
        query2 = """INSERT INTO moderator ( naam, e_mail_adres)
                           VALUES (%s, %s);"""
        data = (keuring, datum_string, tijd_string)
        data1 = (lines[3], lines[2], lines[0], lines[1], lines[4])
        data2 = (naam, e_mail)
        cursor.execute(query, data)
        cursor.execute(query1, data1)
        cursor.execute(query2, data2)
        conn.commit()
        conn.close()
        lijst1 = lijst[1:]
        keuring = ""
        with open("kaas.csv", "w", newline='') as f:
            write = csv.writer(f)
            write.writerows(lijst1)
def moderator_end(naam, e_mail, keuring):
    moderator_naam = naam
    moderator_e_mail = e_mail
    moderator_keuring = keuring
    print("kaas")

def root_clear():
        '''Maakt GUI leeg'''
        for widget in root.winfo_children():
            widget.destroy()


def bericht_achtergelaten():
    root_clear()
    frame = Frame(master=root,
                   background="yellow",
                   height=300)
    label = Label(master=frame,
                  text="NS Station /station/",
                  height=2,
                  background='yellow',
                  font=("helvetica",12,"bold"),
                  foreground='blue')
    label.pack()
    frame.pack(ipadx=300, ipady=8, pady=(0, 70))

    frame1 = Frame(master=root,
                   background= 'yellow',
                   height=400)

    label1 = Label(master=frame1,
                   text="Bericht succesvol verzonden!",
                   background='white',
                   font=("helvetica",16, 'bold'),
                   foreground='blue',
                   padx=20)
    label1.grid(pady=(0,10), column=0, row=0, columnspan=2)
    label2 = Label(master=frame1,
                   text="Het bericht is succesvol verzonden,\nen zal binnenkort beoordeeld worden",
                   background='yellow',
                   font=("helvetica",12, 'bold'),
                   foreground='blue',
                   padx=20)
    label2.grid(pady=(0,10), column=0, row=1, columnspan=2)
    frame1.pack(pady=(0, 70))


def gebruikersvragen():

    root_clear()
    frame = Frame(master=root,
                   background="yellow",
                   height=300)
    label = Label(master=frame,
                  text="NS Station /station/",
                  height=2,
                  background='yellow',
                  font=("helvetica",12,"bold"),
                  foreground='blue')
    label.pack()
    frame.pack(ipadx=300, ipady=8, pady=(0, 70))


    frame1 = Frame(master=root,
                   background= 'yellow',
                   height=400)

    label1 = Label(master=frame1,
                   text="Laat hier uw opmerking achter!",
                   background='white',
                   font=("helvetica",16, 'bold'),
                   foreground='blue',
                   padx=20)
    label1.grid(pady=(0,10), column=0, row=0, columnspan=2)
    label2 = Label(master=frame1,
                   text="Naam:",
                   foreground='blue',
                   font=("Helvetica", 12, 'bold'),
                   background='yellow')
    label2.grid(padx=20, column=0, row= 1, sticky="w")
    label3 = Label(master=frame1,
                   text="Bericht:",
                   foreground='blue',
                   font=("Helvetica", 12, 'bold'),
                   background='yellow')
    label3.grid(padx=20, pady=20, row=2, column=0, sticky="w")

    entry = Entry(master=frame1)
    entry.grid(column=1, row=1)

    entry1 = Entry(master=frame1)
    entry1.grid(column=1, row=2)

    button = Button(master=frame1,
                    text="verzenden",
                    background="blue",
                    foreground="yellow",
                    command=lambda: standaarvragen(entry.get(), entry1.get()))
    button.grid(row=3, column=0, columnspan=2, pady=(0, 20))


    frame1.pack(pady=(0, 70))



    root.mainloop()

def moderator_scherm_inlog():
    root_clear()
    frame = Frame(master=root,
                   background="yellow",
                   height=300)
    label = Label(master=frame,
                  text="NS Station /station/",
                  height=2,
                  background='yellow',
                  font=("helvetica",12,"bold"),
                  foreground='blue')
    label.pack()
    frame.pack(ipadx=300, ipady=8, pady=(0, 70))
    frame1 = Frame(master=root,
                   background= 'yellow',
                   height=400)

    label1 = Label(master=frame1,
                   text="Moderator inlog",
                   background='white',
                   font=("helvetica",16, 'bold'),
                   foreground='blue',
                   padx=20)
    label1.grid(pady=(0,10), column=0, row=0, columnspan=2)
    label2 = Label(master=frame1,
                   text="Naam:",
                   foreground='blue',
                   font=("Helvetica", 12, 'bold'),
                   background='yellow')
    label2.grid(padx=20, column=0, row= 1, sticky="w")
    label3 = Label(master=frame1,
                   text="E-mail",
                   foreground='blue',
                   font=("Helvetica", 12, 'bold'),
                   background='yellow')
    label3.grid(padx=20, pady=20, row=2, column=0, sticky="w")

    entry = Entry(master=frame1)
    entry.grid(column=1, row=1)

    entry1 = Entry(master=frame1)
    entry1.grid(column=1, row=2)

    button = Button(master=frame1,
                    text="verzenden",
                    background="blue",
                    foreground="yellow",
                    command=lambda: moderator_start(entry.get(), entry1.get(), "leeg"))
    button.grid(row=3, column=0, columnspan=2, pady=(0, 20), padx=200)


    frame1.pack(pady=(0, 70))
def moderator_scherm(naam, bericht, e_mail,naam_mod):

    root_clear()
    frame = Frame(master=root,
                  background="yellow",
                  height=300)
    label = Label(master=frame,
                  text="NS Station /station/",
                  height=2,
                  background='yellow',
                  font=("helvetica", 12, "bold"),
                  foreground='blue')
    label.pack()
    frame.pack(ipadx=300, ipady=8, pady=(0, 70))


    frame1 = Frame(master=root,
                   background= 'yellow',
                   height=400)

    label1 = Label(master=frame1,
                   text="Moderator beoordeling",
                   background='white',
                   font=("helvetica",16, 'bold'),
                   foreground='blue',
                   padx=20)
    label1.grid(pady=(0,10), column=0, row=0, columnspan=2)
    label2 = Label(master=frame1,
                   text="Naam:",
                   foreground='blue',
                   font=("Helvetica", 12, 'bold'),
                   background='yellow')
    label2.grid(padx=20, column=0, row= 1, sticky="w")
    label3 = Label(master=frame1,
                   text="bericht",
                   foreground='blue',
                   font=("Helvetica", 12, 'bold'),
                   background='yellow')
    label3.grid(padx=20, pady=20, row=2, column=0, sticky="w")

    label4 = Label(master=frame1,
                   text=naam,
                   foreground='blue',
                   font=("Helvetica", 12, 'bold'),
                   background='yellow')
    label4.grid(column=1, row=1)

    label5 = Label(master=frame1,
                   text=bericht,
                   foreground='blue',
                   font=("Helvetica", 12, 'bold'),
                   background='yellow')
    label5.grid(column=1, row=2)

    button = Button(master=frame1,
                    text="Goedkeuren",
                    background="blue",
                    foreground="yellow",
                    command=lambda: moderator_start(naam_mod, e_mail, "goedgekeurd"))
    button.grid(row=3, column=0, pady=(0, 20))
    button1 = Button(master=frame1,
                    text="Afkeuren",
                    background="blue",
                    foreground="yellow",
                    command=lambda: moderator_start(naam_mod, e_mail, "afgekeurd "))

    button1.grid(row=3, column=1, pady=(0, 20) )

    frame1.pack(pady=(0, 70))

def moderator_eind_scherm():
    root_clear()
    frame = Frame(master=root,
                   background="yellow",
                   height=300)
    label = Label(master=frame,
                  text="NS Station /station/",
                  height=2,
                  background='yellow',
                  font=("helvetica",12,"bold"),
                  foreground='blue')
    label.grid(pady=(0,10), column=0, row=0, columnspan=2)
    frame.grid(pady=(0,10), column=0, row=0, columnspan=2)

    frame1 = Frame(master=root,
                   background= 'yellow',
                   height=400)
    frame1.grid(pady=(0,10), column=0, row=0, columnspan=2)
    label1 = Label(master=frame1,
                   text="moderator",
                   background='white',
                   font=("helvetica",16, 'bold'),
                   foreground='blue',
                   padx=20)
    label1.grid(pady=(0,10), column=0, row=0, columnspan=2)
    label2 = Label(master=frame1,
                   text="Er zijn berichten meer om te beoordelen",
                   background='yellow',
                   font=("helvetica",12, 'bold'),
                   foreground='blue',
                   padx=20)
    label2.grid(pady=(0,10), column=0, row=1, columnspan=2)


def station_scherm():
    naamlijst = []
    berichtlijst = []
    stationlijst = []
    conn = psycopg2.connect(connection_string)  # get a connection with the database
    cursor = conn.cursor()
    query = """select bericht, naam , review.tijd , review.datum, station
                from keuring, review
                where keuring.keuring_id = review.keuring_id
                and keuring.goed_afgekeurd = 'goedgekeurd'
                ORDER BY review.datum, review.tijd Desc
                limit 5;"""  # the st
    cursor.execute(query)
    records = cursor.fetchall()  # retrieve the records from the database
    conn.close()
    print(records)
    for record in records:
        naamlijst.append(record[1])
        berichtlijst.append(record[0])
        stationlijst.append(record[4])
    print(naamlijst)
    print(berichtlijst)
    print(stationlijst)




    root_clear()
    root.geometry("600x400")


    frame = Frame(master=root,
                  background="yellow",
                  height=300)
    label = Label(master=frame,
                  text="NS Station /station/",
                  height=2,
                  background='yellow',
                  font=("helvetica", 12, "bold"),
                  foreground='blue')
    label.pack()
    frame.pack(ipadx=300, ipady=8, pady=(0, 0))


    frame2 = Frame(master=root,
                  background="white",
                  height=300)
    label2 = Label(master=frame2,
                  text="NS Station /station/",
                  height=2,
                  background='white',
                  font=("helvetica", 12, "bold"),
                  foreground='blue')
    label2.pack()
    frame2.pack(ipadx=300, ipady=8, pady=(0, 70))

    frame1 = Frame(master=root,
                   height=400,
                   width=20,
                   background="blue",
                   )
    kaas = ["kaas","kaas1","kaas2", "kaas3", "kaas4"]
    for frame in range(0,5):


        coolframe = Frame(master= frame1,
                          width= 20)
        label1 = Label(master=coolframe,
                       text=naamlijst[frame],
                       background='white',
                       font=("helvetica", 12, 'bold'),
                       foreground='blue',
                       width=10)
        label1.grid()
        label2 = Label(master=coolframe,
                       text="Station: {}".format(stationlijst[frame]),
                       foreground='blue',
                       font=("Helvetica", 8, 'bold'),
                       background='grey',
                       width=10)
        label2.grid()
        label3 = Label(master=coolframe,
                       text= berichtlijst[frame],
                       foreground='blue',
                       font=("Helvetica", 12, 'bold'),
                       background='yellow',
                       wraplength=100,
                       width=10)
        label3.grid()
        coolframe.grid(sticky="w",column=frame, row=0, padx=5)




    frame1.pack()


def startscherm():
    blue_frame = tkinter.Frame(bd=0, highlightthickness=0, background='blue')
    yellow_frame = tkinter.Frame(bd=0, highlightthickness=0, background='yellow')
    yellow_frame1 = tkinter.Frame(bd=0, highlightthickness=0, background='yellow')
    yellow_frame.place(x=0, y=0, relwidth=1, relheight=.25, anchor="nw")
    blue_frame.place(x=0, rely=.25, relwidth=1, relheight=.75, anchor="nw")
    yellow_frame1.place(relx=0.19, rely=0.4, relwidth=0.62, relheight=.5, anchor="nw")

    label = Label(master=root,
                  text="NS Startscherm",
                  height=2,
                  background='yellow',
                  font=("helvetica",12,"bold"),
                  foreground='blue')
    label.pack(side=TOP, padx=20, pady=40)
    label1 = Label(master=root,
                   text="Kies 1 van onderstaande opties:",
                   background='white',
                   font=("helvetica",12, 'bold'),
                   foreground='blue')
    label1.pack(ipady=10, ipadx=60)

    button1 = Button(master=root,
                     text="Stationscherm",
                     background='blue',
                     foreground='white',
                     command=station_scherm
                     )
    button1.pack(ipadx=20, ipady=10,pady=3)

    button2 = Button(master=root,
                     text="Moderator",
                     background='blue',
                     foreground='white',
                     command=moderator_scherm_inlog
                     )
    button2.pack(ipadx=20, ipady=10,pady=3)

    button3 = Button(master=root,
                     text="Bericht achterlaten",
                     background='blue',
                     foreground='white',
                     command= gebruikersvragen)
    button3.pack(ipadx=20, ipady=10,pady= 3)
    root.geometry("600x400")
    root.mainloop()


startscherm()