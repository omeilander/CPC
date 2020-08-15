# -*- coding: utf-8 -*-
"""
Created on Sat Jun 21 19:48:45 2020

@author: omeil
"""

from tkinter import *
from tkinter import messagebox
import numpy
import sqlite3
import csv
import sys

root = Tk()
root.title('Add Members and Exec')
root.iconbitmap("logo.ico")

global names
names = ""

#======================================================================================================

def AddMem(idnum):
    global names
    conn = sqlite3.connect("../Attendance_Sheets_CPC/Master.sqlite")
    c = conn.cursor()

    if len(idnum) > 12:
        idnum = idnum[4:10]

    elif len(idnum) > 6:
        idnum = idnum[4:-3]

    swipe.delete(0, END)

    c.execute("SELECT * FROM Master WHERE id_num = " + idnum)
    records = c.fetchall()

    for record in records:
        ID = records[0]
        first = record[1]
        last = record[2]

    name = first + " " + last + " (id number = " + str(idnum) + ") was added as a member\n"
    names += name
    lab = Label(root, text = names).grid(row = 6, column = 0, columnspan = 5)

    c.execute("""UPDATE Master SET
    gen_member = :points_

    WHERE id_num = :idnum
    """,
              {
                  'points_': 1,
                  'idnum': idnum
              })

    conn.commit()


def SubMem(idnum):
    global names
    conn = sqlite3.connect("../Attendance_Sheets_CPC/Master.sqlite")
    c = conn.cursor()

    if len(idnum) > 12:
        idnum = idnum[4:10]

    elif len(idnum) > 6:
        idnum = idnum[4:-3]

    swipe.delete(0, END)

    c.execute("SELECT * FROM Master WHERE id_num = " + idnum)
    records = c.fetchall()

    for record in records:
        ID = records[0]
        first = record[1]
        last = record[2]

    name = first + " " + last + " (id number = " + str(idnum) + ") was removed as a member\n"
    names += name
    lab = Label(root, text = names).grid(row = 6, column = 0, columnspan = 5)

    c.execute("""UPDATE Master SET
    gen_member = :points_

    WHERE id_num = :idnum
    """,
              {
                  'points_': 0,
                  'idnum': idnum
              })

    conn.commit()


def AddExec(idnum):
    global names
    conn = sqlite3.connect("../Attendance_Sheets_CPC/Master.sqlite")
    c = conn.cursor()

    if len(idnum) > 12:
        idnum = idnum[4:10]

    elif len(idnum) > 6:
        idnum = idnum[4:-3]

    swipe.delete(0, END)

    c.execute("SELECT * FROM Master WHERE id_num = " + idnum)
    records = c.fetchall()

    for record in records:
        ID = records[0]
        first = record[1]
        last = record[2]

    name = first + " " + last + " (id number = " + str(idnum) + ") was added as an exec member\n"
    names += name
    lab = Label(root, text = names).grid(row = 6, column = 0, columnspan = 5)

    c.execute("""UPDATE Master SET
    exec = :points_

    WHERE id_num = :idnum
    """,
              {
                  'points_': 1,
                  'idnum': idnum
              })

    conn.commit()


def SubExec(idnum):
    global names
    conn = sqlite3.connect("../Attendance_Sheets_CPC/Master.sqlite")
    c = conn.cursor()

    if len(idnum) > 12:
        idnum = idnum[4:10]

    elif len(idnum) > 6:
        idnum = idnum[4:-3]

    swipe.delete(0, END)

    c.execute("SELECT * FROM Master WHERE id_num = " + idnum)
    records = c.fetchall()

    for record in records:
        ID = records[0]
        first = record[1]
        last = record[2]

    name = first + " " + last + " (id number = " + str(idnum) + ") was removed as an exec member\n"
    names += name
    lab = Label(root, text = names).grid(row = 6, column = 0, columnspan = 5)

    c.execute("""UPDATE Master SET
    exec = :points_

    WHERE id_num = :idnum
    """,
              {
                  'points_': 0,
                  'idnum': idnum
              })

    conn.commit()

#======================================================================================================

def check(idnum):
    global names
    conn = sqlite3.connect("../Attendance_Sheets_CPC/Master.sqlite")
    c = conn.cursor()

    if len(idnum) > 12:
        idnum = idnum[4:10]

    elif len(idnum) > 6:
        idnum = idnum[4:-3]

    swipe.delete(0, END)

    c.execute("SELECT * FROM Master WHERE id_num = " + idnum)
    records = c.fetchall()
    for record in records:
        idnum = record[0]
        first = record[1]
        last = record[2]
        exe = record [3]
        gen = record[4]
        points_ = record[5]

    main = Toplevel()
    main.iconbitmap("logo.ico")
    main.title('Info')

    def ded():
        main.destroy()
    button_exit = Button(main, text = "Exit", padx = 20 , pady = 10, command = ded).grid(row = 6, column = 2, pady = 10)

    name = "Name: " + first + " " + last
    namel = Label(main, text = name).grid(row = 0, column = 0, columnspan = 5, padx = 10 , pady = 10)
    idm = "ID Number: " + str(idnum)
    idl = Label(main, text = idm).grid(row = 1, column = 0, columnspan = 5, padx = 10 , pady = 10)
    
    if (gen == 1):
        genm = first + " is a Gen Member."
    else:
        genm = first + " is NOT a Gen Member."
    genl = Label(main, text = genm).grid(row = 2, column = 0, columnspan = 5, padx = 10 , pady = 10)
    
    if (exe == 1):
        execm = first + " is an Exec Member."
    else:
        execm = first + " is NOT an Exec Member."
    execl = Label(main, text = execm).grid(row = 3, column = 0, columnspan = 5, padx = 10 , pady = 10)
    
    points = str(points_)
    if (points == "0"):
        poim = first + " doesn't have any points. That's so sad... Alexa play Despicito :,("
    else:
        poim = first + " has " + points + " points."
    poil = Label(main, text = poim).grid(row = 4, column = 0, columnspan = 5, padx = 10 , pady = 10)

    

#======================================================================================================

l = Label(root, text = "Enter the id numbers or have new members/new exec swipe and click 'Add' or 'Remove'").grid(row = 0, column = 0, columnspan = 5, padx = 10 , pady = 10)
swipe = Entry(root, width = 70)
swipe.grid(row = 1, column = 0, columnspan = 5, padx = 20, pady = 10)

addmem = Button(root, text = "Add Gen Member", padx = 20 , pady = 10, command = lambda: AddMem(swipe.get())).grid(row = 2, column = 1, pady = 10)
submem = Button(root, text = "Remove Gen Member", padx = 20 , pady = 10, command = lambda: SubMem(swipe.get())).grid(row = 2, column = 3, pady = 10)

addexec = Button(root, text = "Add Exec Member", padx = 20 , pady = 10, command = lambda: AddExec(swipe.get())).grid(row = 3, column = 1, pady = 10)
subexec = Button(root, text = "Remove Exec Member", padx = 20 , pady = 10, command = lambda: SubExec(swipe.get())).grid(row = 3, column = 3, pady = 10)

button_check = Button(root, text = "Check ID Number", padx = 20 , pady = 10, command = lambda: check(swipe.get())).grid(row = 4, column = 2, pady = 10)
button_exit = Button(root, text = "Exit", padx = 20 , pady = 10, command = root.quit).grid(row = 5, column = 2, pady = 10)




root.mainloop()
