from tkinter import *
import add_win
import sqlite3


def create_table(curs):
    curs.execute('CREATE TABLE IF NOT EXISTS to_do( id INTEGER, date DATE, title TEXT, notes TEXT, recur INT)')


def remove_items():
    print('do stuff')


def add_items(conn, curs):

    root = Tk()

    window = add_win.Window(root, conn, curs)

    root.mainloop()


def main(arg):
    conn = sqlite3.connect('to_do.db')
    curs = conn.cursor()

    create_table(curs)

    if arg == '-add':
        add_items(conn, curs)
    '''
    elif arg == '-myweek':
        display_date_range(next 7 days):
    elif arg == '-lookup':
        interactive_lookup():
    elif arg == '-upcoming':
        display_date_range(display all from today until the end of the todo list)
    elif arg == '-past':
        display_date_range(display all from start of database until today)
    else:
        display_help()
    '''

main('-add')