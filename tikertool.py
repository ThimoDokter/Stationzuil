import psycopg2
from tkinter import *
connection_string = "host='localhost' dbname='stationzuil2' user='postgres' password='kaas'"
conn = psycopg2.connect(connection_string)  # get a connection with the database
cursor = conn.cursor()

query =""" SELECT bericht, naam , review.tijd , review.datum
           from keuring, review
           where keuring.keuring_id = review.keuring_id
           and keuring.goed_afgekeurd = 'afgekeurd'"""

cursor.execute(query)
records = cursor.fetchall()
for record in records:
    print(record[0])

print(records)
print(records[0][1])


root = Tk()



label = Label(master=root,
              text="bericht 1:",
              background='yellow')
label.pack()
label1 = Label(master= root,
               text=f'{records[0][0]}\n {records[0][1]}',
               background='yellow')
label1.pack()

root.mainloop()