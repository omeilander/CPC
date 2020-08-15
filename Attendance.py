# -*- coding: utf-8 -*-
"""
Created on Sat Jun 13 19:48:45 2020

@author: omeil
"""

from tkinter import *
from tkinter import messagebox
import numpy
import sqlite3
import csv
import sys

root = Tk()
root.title('CPC Attendance Sheet')
root.iconbitmap("logo.ico")

global conn
global c
conn = sqlite3.connect("../Attendance_Sheets_CPC/Master.sqlite")
c = conn.cursor()

global counter
counter = 0

global names
names = ""


def daEnd(x):
    global name_
    global counter
    
    newcon = sqlite3.connect(name_)
    c2 = newcon.cursor()

    c2.execute("SELECT * FROM Attendance")
    result = c2.fetchall()

    filename = "../Attendance_Sheets_cpc" + name_[12:-6] + "csv"
    with open(filename, 'a') as f:
        w = csv.writer(f, dialect = "excel")

        endnum = "Number in Attendance: " + str(counter)
        firstwrite = ["Id Number", "First/Middle Name", "Last Name", "Exec", "Gen Member", "Helped", "Points", "", endnum]
        w.writerow(firstwrite)
        for record in result:
            w.writerow(record)

    sys.exit()

def submit(ty, na, mon, day, year):
    global points
    global conn
    global c
    global counter
    global name_

    names = "" 

    na = na.lower().replace(" ", "_")
    name_ = "../cpc_trash/" + str(mon) + "_" + str(day) + "_" + str(year) + "_" + na + ".sqlite"
    newcon = sqlite3.connect(name_)
    c2 = newcon.cursor()
    
    c2.execute("""CREATE TABLE Attendance (
        "id_num" text,
        "first_middle_name" text,
        "last_name" text,
        "exec" integer,
        "gen_member" integer,
        "helped" integer,
        "points" integer
)
""")

    

    def addpoint(p):
        global point
        global points
        points = int(p)
        point.destroy()

    
    if (ty == "Rotational"):
        points = 10
        
    elif (ty == "First Friday"):
        points = 10
        
    elif (ty == "Movie"):
        points = 10
        
    elif (ty == "Gen Meeting"):
        points = 10

    else:
        global point
        point = Toplevel()
        point.title('Other points?')

        l = Label(point, text = "How many points is this event worth?").grid(row = 0, column = 0, columnspan = 5, padx = 10 , pady = 10)
        number = Entry(point, width = 20)
        number.grid(row = 1, column = 0, columnspan = 5, padx = 20, pady = 10)
        sub = Button(point, text = "Submit", padx = 20 , pady = 10, command = lambda: addpoint(number.get())).grid(row = 2, column = 2, pady = 10)


    def add(idnum, Help):
        global name_
        global names
        global points
        global counter

        if len(idnum) > 12:
            idnum = idnum[4:10]

        elif len(idnum) > 6:
            idnum = idnum[4:-3]
            
        conn = sqlite3.connect("../Attendance_Sheets_CPC/Master.sqlite")
        c = conn.cursor()
        newcon = sqlite3.connect(name_)
        c2 = newcon.cursor()

        check.deselect()
        swipe.delete(0, END)

        c.execute("SELECT * FROM Master WHERE id_num = " + idnum)
        records = c.fetchall()

        def addperson(idnum, Help, first, last, gen, exe = 0, poi = 0):
            global name_
            global names
            global nohave
            global points
            global counter
            nohave.destroy()

            points_ = points
            conn = sqlite3.connect("../Attendance_Sheets_CPC/Master.sqlite")
            c = conn.cursor()
            newcon = sqlite3.connect(name_)
            c2 = newcon.cursor()

            c.execute("INSERT INTO Master VALUES (:id_num, :first_middle_name, :last_name, :exec, :gen_member, :points)",
                   {
                       'id_num' : idnum,
                       'first_middle_name' : first,
                       'last_name' : last,
                       'exec' : exe,
                       'gen_member' : gen,
                       'points' : poi
                   }
            )

            c2.execute("INSERT INTO Attendance VALUES (:id_num, :first_middle_name, :last_name, :exec, :gen_member, :helped, :points)",
                   {
                       'id_num' : idnum,
                       'first_middle_name' : first,
                       'last_name' : last,
                       'exec' : exe,
                       'gen_member' : gen,
                       'helped' : Help,
                       'points' : poi
                   }
            )#update (and make) counter
            counter += 1
            count.delete(0, END)
            count.insert(0, str(counter))

            name = first + " " + last + "\n"
            names += name
            here_label = Label(current, text = names).grid(row = 3, column = 0, columnspan = 5)

            #update current points
            c.execute("""UPDATE Master SET
            points = :points_

            WHERE id_num = :idnum
            """,
                  {
                      'points_': points_,
                      'idnum': idnum
                  })

            conn.commit()
            newcon.commit()
            
            
        if len(records) == 0:
            global nohave 
            nohave = Toplevel()
            nohave.iconbitmap("logo.ico")
            l = Label(nohave, text = "We don't have you in our system!! We need some info real quick!")
            l.grid(row = 0, column = 0, columnspan = 5, padx = 10 , pady = 10)
            f_l = Label(nohave, text = "First Name").grid(row = 1, column = 0)
            l_l = Label(nohave, text = "Last Name").grid(row = 2, column = 0)
            genmem_l = Label(nohave, text = "Gen Member?").grid(row = 3, column = 0)
            
            f_b = Entry(nohave, width = 30)
            f_b.grid(row = 1, column = 1)
            l_b = Entry(nohave, width = 30)
            l_b.grid(row = 2, column = 1)
            general = IntVar()
            genmem_b = Checkbutton(nohave, variable = general)
            genmem_b.grid(row = 3, column = 1)

            submit_new = Button(nohave, text = "Submit", command = lambda: addperson(idnum, Help, f_b.get(), l_b.get(), general.get())).grid(row = 4, column = 1, padx = 10 , pady = 10)

        else:
            for record in records:
                idnum = record[0]
                first = record[1]
                last = record[2]
                exe = record [3]
                gen = record[4]
                points_ = record[5]
                points_ += points

            if (Help == 1):
                points_ += 5

            c2.execute("INSERT INTO Attendance VALUES (:id_num, :first_middle_name, :last_name, :exec, :gen_member, :helped, :points)",
                   {
                       'id_num' : idnum,
                       'first_middle_name' : first,
                       'last_name' : last,
                       'exec' : exe,
                       'gen_member' : gen,
                       'helped' : Help,
                       'points' : points_
                   }
            )
        
            #update (and make) counter
            counter += 1
            count.delete(0, END)
            count.insert(0, str(counter))

            name = first + " " + last + "\n"
            names += name
            here_label = Label(current, text = names).grid(row = 3, column = 0, columnspan = 5)

            #update current points
            c.execute("""UPDATE Master SET
            points = :points_

            WHERE id_num = :idnum
            """,
                  {
                      'points_': points_,
                      'idnum': idnum
                  })
        
        conn.commit()
        newcon.commit()
        c.close()
        c2.close()
        return   

        
    main = Toplevel()
    main.iconbitmap("logo.ico")
    main.title('Swipe, Swipe, Swipe!')

    Help = IntVar()
    l = Label(main, text = "Have student swipe and then hit 'Submit'").grid(row = 0, column = 0, columnspan = 5, padx = 10 , pady = 10)
    swipe = Entry(main, width = 70)
    swipe.grid(row = 1, column = 0, columnspan = 5, padx = 20, pady = 10)
    check = Checkbutton(main, text = "Check if they helped", variable = Help, offvalue = 0, onvalue = 1)
    check.grid(row = 2, column = 0, columnspan = 5, padx = 10 , pady = 10)
    check.deselect()
    
    sub = Button(main, text = "Submit", padx = 20 , pady = 10, command = lambda: add(swipe.get(), Help.get()))
    sub.grid(row = 3, column = 1, pady = 10)
    end = Button(main, text = "End Program", padx = 20 , pady = 10, command = lambda: daEnd(1))
    end.grid(row = 3, column = 3, pady = 10)
    
    def addsub(crap):
        q = add(swipe.get(), Help.get())
    swipe.bind("<Return>", addsub)

    current = Toplevel()
    current.title('Right now we have...')
    current.iconbitmap("logo.ico")
    current.title('Current Attendance')
    l1 = Label(current, text = "Total number in attendance:").grid(row = 0, column = 0, columnspan = 5, padx = 20, pady = 10)
    count = Entry(current, width = 20)
    count.grid(row = 1, column = 0, columnspan = 5)
    l2 = Label(current, text = "These are the students currently swiped in: ").grid(row = 2, column = 0, columnspan = 5, padx = 20, pady = 10)

    
    newcon.commit()
    main.mainloop()
    #newcon.close()
    

    
#======================================================================================================

"""

"""

intro = "It's already time for another event?! Well lets get started"
    
l = Label(root, text = intro).grid(row = 0, column = 0, columnspan = 5, padx = 10 , pady = 20)

eventtype = StringVar()
eventtype.set("Rotational")
listofevents = ["Rotational", "First Friday", "Movie", "Gen Meeting", "Other"]
typeofevent = OptionMenu(root, eventtype, *listofevents)
typeofevent.grid(row = 2, column = 1, columnspan = 3, padx = 10)

toe_l = Label(root, text = "Type of event:").grid(row = 1, column = 2)
nameofevent = Entry(root, width = 70)
nameofevent.grid(row = 5, column = 0, columnspan = 5, padx = 20)
noe_l = Label(root, text = "Name of event:").grid(row = 4, column = 2)
Label(root, text = " ").grid(row = 3, column = 0)
Label(root, text = " ").grid(row = 6, column = 0)
Label(root, text = " ").grid(row = 9, column = 0)

month = IntVar()
month.set(8)
n_m = numpy.arange(1, 13, 1)
month_ = OptionMenu(root, month, *n_m)
month_.grid(row = 7, column = 0, padx = 10 , pady = 10)
m_l = Label(root, text = "Month").grid(row = 8, column = 0, padx = 10)
day = IntVar()
day.set(16)
n_d = numpy.arange(1, 32, 1)
day_ = OptionMenu(root, day, *n_d)
day_.grid(row = 7, column = 2, padx = 10 , pady = 10)
d_l = Label(root, text = "Day").grid(row = 8, column = 2, padx = 10)
year = IntVar()
year.set(2020)
n_y = numpy.arange(2020, 2031, 1)
year_ = OptionMenu(root, year, *n_y)
year_.grid(row = 7, column = 4, padx = 10 , pady = 10)
y_l = Label(root, text = "Year").grid(row = 8, column = 4, padx = 10)

button_submit = Button(root, text = "Submit", padx = 20 , pady = 10, command = lambda: submit(eventtype.get(), nameofevent.get(), month.get(), day.get(), year.get())).grid(row = 10, column = 2, pady = 10)


def subsub(crap):
    pp = submit(eventtype.get(), nameofevent.get(), month.get(), day.get(), year.get())
nameofevent.bind("<Return>", subsub)

button_exit = Button(root, text = "Exit", padx = 20 , pady = 10, command = root.quit).grid(row = 11, column = 2, pady = 10)

root.mainloop()
