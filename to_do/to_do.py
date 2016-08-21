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

class Add_window:
    def __init__(self):
        self.master = Tk()

        self.master.title('Add a To Do Item')
        self.master.resizable(width=False, height=False)

        # frames
        self.top_frame = Frame(self.master)
        self.top_frame.pack()

        self.middle_frame = Frame(self.master)
        self.middle_frame.pack()

        self.bottom_frame = Frame(self.master)
        self.bottom_frame.pack()

        # titles
        self.title_label = Label(self.top_frame, text='Title:')
        self.title_label.grid(row=0, sticky=W)

        self.notes_label = Label(self.top_frame, text='Notes:')
        self.notes_label.grid(row=2, sticky=W)

        self.date_label = Label(self.top_frame, text='Date:')
        self.date_label.grid(row=1, sticky=W)

        self.recur_label = Label(self.middle_frame, text='Recurrance:')
        self.recur_label.grid(row=0)

        # entries
        self.title_entry = Entry(self.top_frame)
        self.title_entry.grid(row=0, column=1, sticky=W)

        self.date = StringVar()
        self.date.set('Today')
        self.date_entry = Entry(self.top_frame, textvariable=self.date, state='normal')
        self.date_entry.grid(row=1, column=1, sticky=W)

        self.notes_entry = Entry(self.top_frame, width=50)
        self.notes_entry.grid(row=2, column=1)

        # check buttons
        self.daily_var = IntVar()
        self.daily_recur = Checkbutton(self.middle_frame, text='dy', variable=self.daily_var)
        self.daily_recur.grid(row=0, column=1)

        self.weekly_var = IntVar()
        self.weekly_recur = Checkbutton(self.middle_frame, text='wk', variable=self.weekly_var)
        self.weekly_recur.grid(row=0, column=2)

        self.monthly_var = IntVar()
        self.monthly_recur = Checkbutton(self.middle_frame, text='mn', variable=self.monthly_var)
        self.monthly_recur.grid(row=0, column=3)

        self.yearly_var = IntVar()
        self.yearly_recur = Checkbutton(self.middle_frame, text='yr', variable=self.yearly_var)
        self.yearly_recur.grid(row=0, column=4)

        #buttons
        self.add_button = Button(self.bottom_frame, text='add', command=lambda: self.write_to_db())
        self.add_button.grid(row=0, column=0)

        self.done_button = Button(self.bottom_frame, text='done', command=self.master.destroy)
        self.done_button.grid(row=0, column=1, sticky=E)

        self.cal_button = Button(self.top_frame, text='CAL', relief=FLAT, command=lambda: self.interactive_cal())
        self.cal_button.grid(row=1, column=1)

        self.master.mainloop()

    def interactive_cal(self):
        #self.date.set(dyn_calendar.open_calendar())
        print('process stopped')
        print(self.date.get())



    def write_to_db(self):
        global conn
        global curs

        data = []
        # load data into tuple
        if self.date.get() == 'Today': # entry field defaults to today's date
            data.append(datetime.date.today())
        else:
            data.append(self.date.get())

        data.append(self.title_entry.get())
        data.append(self.notes_entry.get())
        data.append(self.daily_var.get())
        data.append(self.weekly_var.get())
        data.append(self.monthly_var.get())
        data.append(self.yearly_var.get())

        for x in range(len(data)):
            print(data[x])

        # write to to_do.db
        curs.execute('''INSERT INTO to_do VALUES(?, ?, ?, ?, ?, ?, ? )''', (data[0], data[1], data[2], data[3],
                                                                              data[4], data[5], data[6]))
        conn.commit()

        # clear all fields
        self.title_entry.delete(0, 'end')
        self.date_entry.delete(0, 'end')
        self.notes_entry.delete(0, 'end')
        self.daily_recur.deselect()
        self.weekly_recur.deselect()
        self.monthly_recur.deselect()
        self.yearly_recur.deselect()


#def display_help():

#def interactive_lookup():

#def display_date_range():



#remove_to_do():



def create_table():
    global curs
    curs.execute('CREATE TABLE IF NOT EXISTS to_do( date DATE, title TEXT, notes TEXT, d INTEGER, w INTEGER, m '
                   'INTEGER, y INTEGER )')

def main(arg):
    global conn
    global curs

    create_table()

    if arg == '-add':
        window = Add_window()
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


today = datetime.datetime.now()


main('-add')
