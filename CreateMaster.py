# -*- coding: utf-8 -*-
"""
Created on Sat Jun 13 19:48:45 2020

@author: omeil
"""

import sqlite3
import csv

conn = sqlite3.connect('Master.sqlite')
cur = conn.cursor()

cur.execute('DROP TABLE IF EXISTS Master')
cur.execute("""
CREATE TABLE Master(
        "id_num" text,
        "first_middle_name" text,
        "last_name" text,
        "exec" integer,
        "gen_member" integer,
        "points" integer
)
""")


fname = "everyone.csv"


with open(fname) as csv_file:
    csv_reader = csv.reader(csv_file, delimiter = ',')
    for row in csv_reader:
        #print(row)
        id_num = row[0]
        first_middle_name = row[1]
        last_name = row[2]
        exec = int(row[3])
        gen_member = int(row[4])
        points = int(row[5])
        cur.execute("""INSERT INTO Master(id_num, first_middle_name, last_name, exec, gen_member, points) VALUES (?,?,?,?,?,?)""",
                    (id_num, first_middle_name, last_name, exec, gen_member, points))
        conn.commit()

