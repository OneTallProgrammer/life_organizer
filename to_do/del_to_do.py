# standard libraries
import datetime
import sqlite3
import os
from tkinter import *

# user defined libraries
import dyn_calendar

#here = os.path.dirname(os.path.abspath(__file__))

#global variables because every function listed will need to access this database
conn = sqlite3.connect('to_do.db')
curs = conn.cursor()

#def display_help():

#def interactive_lookup():

#def display_date_range():



#remove_to_do():

def create_table():
    global curs
    curs.execute('CREATE TABLE IF NOT EXISTS to_do( date DATE, title TEXT, notes TEXT, d INTEGER, w INTEGER, m '
                   'INTEGER, y INTEGER )')




today = datetime.datetime.now()


main('-add')
