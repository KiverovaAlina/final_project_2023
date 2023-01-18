import sqlite3
import pandas as pd

con = sqlite3.connect("patients.sqlite")
f_damp = open('patient.db','r', encoding ='utf-8-sig')
damp = f_damp.read()
f_damp.close()
con.executescript(damp)
con.commit()
cursor = con.cursor()

con.commit()

