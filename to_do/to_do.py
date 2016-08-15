import datetime
import sqlite3
from tkinter import *

class Add_window:
    def __init__(self, master):
        self.master = master
        master.title('Add a To Do Item')

        self.top_frame = Frame(master)
        self.top_frame.pack()

        self.bottom_frame = Frame(master)
        self.bottom_frame.pack()

        self.title = Label(self.top_frame, text='Title:')
        self.title.grid(row=0, sticky=W)

        self.due_by = Label(self.top_frame, text='Due Date:')
        self.due_by.grid(row=2, sticky=W)

        self.title_entry = Entry(self.top_frame)
        self.title_entry.grid(row=0, column=1, sticky=W)

        self.notes = Label(self.top_frame, text='Notes:')
        self.notes.grid(row=1, sticky=W)

        self.notes_entry = Entry(self.top_frame, width=50)
        self.notes_entry.grid(row=1, column=1)

        self.done = Button(self.bottom_frame, text='done', command=master.destroy)
        self.done.grid(row=0, column=1, sticky=E)

        self.due_date = Checkbutton(self.top_frame, text='Completion date', variable=date_bound) #not functional
        self.due_date.grid(row=2, column=1, sticky=W)

    def write_to_db(self, data, cursor, db):
        data = []
        data.append(self.title_entry.get())

        for x in range(len(data)):
            print(data[x])

        #write to to_do.db
        cursor.execute("INSERT INTO to_do VALUES(\"%s\", \"%s\" )" % (data[0], data[1]))
        db.commit()










#def display_help():

#def interactive_lookup():

#def display_date_range():

def add_to_do(db, cursor):
    data = []

    root = Tk()

    window = Add_window(root)

    add = Button(window.bottom_frame, text='add', command=lambda: window.write_to_db(data, cursor, db))
    add.grid(row=0, column=0)

    root.mainloop()

#remove_to_do():

def create_table(cursor):
    cursor.execute('CREATE TABLE IF NOT EXISTS to_do( due_date BOOL, title TEXT, notes TEXT )')

def main(arg):
    conn = sqlite3.connect('to_do.db')
    c = conn.cursor()
    create_table(c)

    if arg == '-add':
        add_to_do(conn, c)
    '''
    elif arg == '-remove':
        remove_to_do()
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
