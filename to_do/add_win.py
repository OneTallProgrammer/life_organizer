from tkinter import *
import datetime
import calendar


class Window:
    def __init__(self, master, db, curs):


        master.title('Add a To Do Item')
        #master.resizable(width=False, height=False)
        #master.minsize(width=550, height=380)

        #link the window to the db
        self.db = db
        self.curs = curs

        # determine th starting length of the database
        self.curs.execute('SELECT * FROM to_do')
        self.db_length = len(self.curs.fetchall())

        # array to hold the current selection of appointments
        self.appts = []

        '''
            general layout formatting
        '''

        # main frames
        self.entry_frame = Frame(master)
        self.entry_frame.grid(row=0, column=0, sticky='NW')

        self.cal_frame = Frame(master, borderwidth=10, bg='white')
        self.cal_frame.grid(row=0, column=1)
        #self.cal_frame.grid_propagate(False)

        self.list_frame = Frame(master)
        self.list_frame.grid(row=1, column=0, columnspan=2)


        '''
            entry field formatting
        '''

        # entry specific frames
        self.top_frame = Frame(self.entry_frame)
        self.top_frame.grid(row=0, column=0, sticky='W')

        self.bottom_frame = Frame(self.entry_frame)
        self.bottom_frame.grid(row=2, column=0, sticky='W')

        # titles
        self.title_label = Label(self.top_frame, text='Title:')
        self.title_label.grid(row=0, sticky='W')

        self.notes_label = Label(self.top_frame, text='Notes:')
        self.notes_label.grid(row=2, sticky='NW')

        self.date_label = Label(self.top_frame, text='Date:')
        self.date_label.grid(row=1, sticky='W')

        self.recur_label = Label(self.top_frame, text='Recurrance:')
        self.recur_label.grid(row=4, sticky='W')

        # entries
        self.title_entry = Entry(self.top_frame, bg='#ffffcc')
        self.title_entry.grid(row=0, column=1)

        self.date = StringVar()
        self.date.set('Today')
        self.date_entry = Entry(self.top_frame, textvariable=self.date, state='disabled', bg='#ffffcc')
        self.date_entry.grid(row=1, column=1)

        self.notes_text = Text(self.top_frame, height=7, width=22, wrap=WORD, bg='#ffffcc')
        self.notes_text.grid(row=2, column=1)

        # check buttons
        self.checkbox_frame = Frame(self.top_frame, borderwidth=3)
        self.checkbox_frame.grid(row=4, column=1)

        self.recur_var = IntVar()

        self.daily_recur = Radiobutton(self.checkbox_frame, variable=self.recur_var, text='dy', value=1)
        self.daily_recur.grid(row=0, column=0)
        self.daily_recur.config(highlightbackground='white')

        self.weekly_recur = Radiobutton(self.checkbox_frame, variable=self.recur_var, text='wk', value=2)
        self.weekly_recur.grid(row=0, column=1)
        self.weekly_recur.config(highlightbackground='white')

        self.monthly_recur = Radiobutton(self.checkbox_frame, variable=self.recur_var, text='mn', value=3)
        self.monthly_recur.grid(row=0, column=2)
        self.monthly_recur.config(highlightbackground='white')

        self.yearly_recur = Radiobutton(self.checkbox_frame, variable=self.recur_var, text='yr', value=4)
        self.yearly_recur.grid(row=0, column=3)
        self.yearly_recur.config(highlightbackground='white')

        #buttons
        self.add_button = Button(self.bottom_frame, text='add', command=lambda: self.write_to_db())
        self.add_button.grid(row=0, column=0)

        self.rem_button = Button(self.bottom_frame, text='remove', command=lambda: self.remove_from_db())
        self.rem_button.grid(row=0, column=1)

        self.done_button = Button(self.bottom_frame, text='done', command=master.destroy)
        self.done_button.grid(row=0, column=2, sticky=E)


        '''
            calendar formatting
        '''

        # calendar specific frames
        self.cal_header = Frame(self.cal_frame, bg='white')
        self.cal_header.grid(row=0, column=0)

        self.day_labels = Frame(self.cal_frame, bg='white')
        self.day_labels.grid(row=1, column=0)

        self.cal_dates = Frame(self.cal_frame, bg='white')
        self.cal_dates.grid(row=2, column=0)

        # calender labels
        self.month_label = Label(self.cal_header, text='', bg='white')
        self.month_label.grid(row=0, column=1)

        self.year_label = Label(self.cal_header, text='', bg='white')
        self.year_label.grid(row=0, column=2)

        # buttons
        self.prev = Button(self.cal_header, text='prev', relief=SOLID, bg='white', command=lambda: self.new_month(-1))
        self.prev.grid(row=0, column=0, )

        self.next = Button(self.cal_header, text='next', relief=SOLID, bg='white', command=lambda: self.new_month(1))
        self.next.grid(row=0, column=3)

        '''
            visual list formatting
        '''
        self.scrollbar = Scrollbar(self.list_frame)
        self.scrollbar.grid(row=0, column=1, sticky='NS')

        self.to_do_list = Listbox(self.list_frame, width=69, yscrollcommand=self.scrollbar.set, bg='#99ccff')
        self.to_do_list.grid(row=0, column=0, sticky='E')

        self.scrollbar.config(command=self.to_do_list.yview)

        '''
            button bindings
        '''

        self.to_do_list.bind("<ButtonRelease-1>", self.display_notes)
        master.bind("<ButtonRelease-1>", self.check_if_updating)
        self.title_entry.bind("<KeyRelease>", self.check_if_updating)


        self.initial_data()

        '''
            interactive calendar member functions
        '''

    def initial_data(self):
        # process to generate and manage calendar
        self.today = datetime.date.today()
        self.year = self.today.year
        self.month = self.today.month
        self.pressed_button = Button()
        self.btn_array = []
        self.cal_data = []

        self.gen_month_data_list()
        self.gen_cal_header()
        self.print_buttons()

        # generate initial data upon opening the widget
        self.select_day(self.today.day)

    def gen_month_data_list(self):
        """
            generates the required data to display calendar information
            :param self: member function of class Window
        """
        self.pressed_button = Button()

        text_cal = calendar.TextCalendar()
        month_string = text_cal.formatmonth(self.year, self.month)
        month_list = month_string.split()

        self.cal_data = month_list

    def gen_cal_header(self):
        """
            sets the month labels at the top of the interactive calendar
            :param self: member function of class Window
        """
        self.month_label.config(text=self.cal_data[0])
        self.year_label.config(text=self.cal_data[1])

    def print_buttons(self):
        """
            prints a set of interactive buttons corresponding to the date of the month currently selected
            :param self: member function of class Window
        """
        self.cal_dates.destroy()
        self.btn_array = []

        self.cal_dates = Frame(self.cal_frame, bg='white')
        self.cal_dates.grid(row=2, column=0)

        self.su_label = Label(self.cal_dates, text='Su', bg='white')
        self.su_label.grid(row=0, column=0)

        self.mo_label = Label(self.cal_dates, text='Mo', bg='white')
        self.mo_label.grid(row=0, column=1)

        self.tu_label = Label(self.cal_dates, text='Tu', bg='white')
        self.tu_label.grid(row=0, column=2)

        self.we_label = Label(self.cal_dates, text='We', bg='white')
        self.we_label.grid(row=0, column=3)

        self.th_label = Label(self.cal_dates, text='Th', bg='white')
        self.th_label.grid(row=0, column=4)

        self.fr_label = Label(self.cal_dates, text='Fr', bg='white')
        self.fr_label.grid(row=0, column=5)

        self.sa_label = Label(self.cal_dates, text='Sa', bg='white')
        self.sa_label.grid(row=0, column=6)

        grid_width = 7
        index = 9

        row = 1

        # checks what day of week the first day of the month falls on
        if calendar.weekday(self.year, self.month, 1) == 6:
            column = 0
        else:
            column = calendar.weekday(self.year, self.month, 1) + 1

        # print the dates as buttons and bind them to a method
        while index < len(self.cal_data):
            new_button = Button(self.cal_dates, text=self.cal_data[index], relief=FLAT, bg='white', command=
            lambda opt=int(self.cal_data[index]):
            self.select_day(opt)
            )

            self.btn_array.append(new_button)

            new_button.grid(row=row, column=column, sticky='E' + 'W')

            index += 1
            column += 1

            if column == grid_width:
                column = 0
                row += 1

    def new_month(self, mod):
        """
            resets all calendar information and generates a new month and displays it
            :param self: member function of class Window
            :param mod: int 1 will move the month to the next following month and -1 will move to the previous
        """
        self.month += mod

        if self.month == 13: # next year
            self.year += 1
            self.month = 1
        elif self.month == 0: # previous year
            self.year -= 1
            self.month = 12

        # generate and print the new month
        self.gen_month_data_list()
        self.gen_cal_header()
        self.print_buttons()


    def select_day(self, day):
        """
            button operation that tracks the selected date visually on calendar
            @ param self: member function of class Window
            @ param date: the selected date
        """
        self.date.set(datetime.date(self.year, self.month, day))
        self.pressed_button['relief'] = FLAT
        self.pressed_button['bg'] = 'white'
        self.btn_array[day - 1]['relief'] = SUNKEN
        self.btn_array[day - 1]['bg'] = '#ffffcc'
        self.pressed_button = self.btn_array[day - 1]

        self.refresh_list()


    def format_string(self, string):
        """
        format a string to remove outer spaces, tab characters, and newline characters
        :param string: the string being formatted
        :return: the formatted string
        """
        characters = list(string)
        index = 0
        while characters[index] == ' ':
            index += 1

        characters = characters[index:]

        index = len(characters) - 1
        while characters[index] == ' ':
            index -= 1

        characters = characters[0:index + 1]

        string = ''.join(characters)

        string = string.replace('\t', '')

        return string

    def display_notes(self, click):
        try:
            index = self.to_do_list.curselection()[0]
        except IndexError:
            return
        else:
            # clear the title and notes entries
            self.title_entry.delete(0, END)
            self.notes_text.delete('0.0', END)

            id = self.appts[index][0]
            self.curs.execute('SELECT title, notes, recur FROM to_do WHERE id=?', (str(id)))

            selection = self.curs.fetchall()


            if len(selection) != 1:
                print('Error displaying fields "title" and "notes": %d records selected' % (len(selection)))
            else:
                selection = selection[0] # strip off outer tuple layer
                title = selection[0]
                notes = selection[1]
                recur = int(selection[2])


                # print to the notes' and title fiels
                self.title_entry.insert(0, title)
                self.notes_text.insert('0.0', notes)

                # set recur option
                self.recur_var.set(recur)

    def refresh_list(self):
        WEEK = 7
        YEAR = 365

        # clear the list and the appts array
        self.appts = []
        self.to_do_list.delete(0, END)

        # select and display daily recurring reminders
        self.curs.execute('SELECT id, title FROM to_do WHERE recur=1')

        for row in self.curs.fetchall():
            self.appts.append(row)  # # save to memory for deletion and indexing purposes
            self.to_do_list.insert(END, 'D: ' + row[1])
            self.to_do_list.itemconfig(END, bg='#e1ffe4')

        # select and display weekly recurring reminders
        self.curs.execute('SELECT id, title, date FROM to_do WHERE recur=2')

        for row in self.curs.fetchall():
            day_1 = datetime.datetime.strptime(row[2], '%Y-%m-%d')
            day_2 = datetime.datetime.strptime(self.date.get(), '%Y-%m-%d')

            if (day_1 - day_2).days % WEEK == 0:
                self.appts.append(row[0:2])  # save to memory for deletion and indexing purposes
                self.to_do_list.insert(END, 'W: ' + row[1])
                self.to_do_list.itemconfig(END, bg='#ffc2b2')

        # select and display monthly recurring reminders
        self.curs.execute('SELECT id, title, date FROM to_do WHERE recur=3')

        for row in self.curs.fetchall():
            # extract day from date string format yyyy-mm-dd
            day_made = int(row[2][8:])
            day_select = int(self.date.get()[8:])
            end_of_month = calendar.monthrange(int(self.date.get()[0:4]), int(self.date.get()[5:7]))[1]

            # if the day is same as the day  of the month that the reminder was created or
            # if its the end of the month and the reminder made at the end of a longer month
            if day_select == day_made or (day_made > day_select and day_select == end_of_month):
                self.appts.append(row[0:2])  # save to memory for deletion and indexing purposes
                self.to_do_list.insert(END, 'M: ' + row[1])
                self.to_do_list.itemconfig(END, bg='#e0d8ff')

        # select and display yearly recurring dates
        self.curs.execute('SELECT id, title, date FROM to_do WHERE recur=4')

        for row in self.curs.fetchall():
            # extract date from string format yyyy-mm-dd
            day_1 = datetime.datetime.strptime(row[2], '%Y-%m-%d')
            day_2 = datetime.datetime.strptime(self.date.get(), '%Y-%m-%d')

            if (day_1 - day_2).days % YEAR == 0:
                self.appts.append(row[0:2])  # save to memory for deletion and indexing purposes
                self.to_do_list.insert(END, 'Y: ' + row[1])
                self.to_do_list.itemconfig(END, bg='orange')

        # select any non-recurring dates on the day selected
        self.curs.execute('SELECT id, title FROM to_do WHERE date=? AND recur=0', (self.date.get(),))

        for row in self.curs.fetchall():
            self.appts.append(row)  # save to memory for deletion and indexing purposes
            self.to_do_list.insert(END, row[1])

        print(self.appts)

    def check_if_updating(self, click):
        try:
            index = self.to_do_list.curselection()[0]
        except IndexError:
            self.add_button.config(text='add', command=lambda: self.write_to_db())
            self.recur_var.set(0)
        else:
            if self.title_entry.get() == self.appts[index][1]:
                self.add_button.config(text='update', command=lambda: self.update_record())

            else:
                self.add_button.config(text='add', command=lambda: self.write_to_db())
                self.recur_var.set(0)

    def update_record(self):
        try:
            index = self.to_do_list.curselection()[0]
        except IndexError:
            return
        else:
            self.curs.execute('UPDATE to_do SET notes=?, recur=? WHERE id=?',
                              (self.notes_text.get('1.0', END),
                               self.recur_var.get(),
                               self.appts[index][0],))

            self.refresh_list()



    def write_to_db(self):
        """
            writes the users information to the selected database
            @ param self: member function of class Window
        """

        # if there is no title, assume the user has not entered it correctly
        if self.title_entry.get() == '':
            return

        data = []

        self.db_length += 1

        data.append(self.db_length)


        # load data into tuple
        if self.date.get() == 'Today': # entry field defaults to today's date
            data.append(datetime.date.today())
        else:
            data.append(self.date.get())


        data.append(self.title_entry.get())
        data.append(self.notes_text.get('1.0', END))
        data.append(self.recur_var.get())

        # remove outer spaces
        data[2] = self.format_string(data[2])
        data[3] = self.format_string(data[3])

        # Delete any duplicate before writing
        #self.curs.execute('DELETE FROM to_do WHERE date=? AND title=?', (data[0], data[1]))




        # write to selected database
        self.curs.execute('INSERT INTO to_do VALUES(?, ?, ?, ?, ? )', (data[0], data[1], data[2], data[3], data[4],))

        self.db.commit()

        # clear all fields
        self.title_entry.delete(0, 'end')
        self.date_entry.delete(0, 'end')
        self.notes_text.delete('1.0', END)

        self.refresh_list()


    def remove_from_db(self):
        try:
            index = self.to_do_list.curselection()[0]
        except IndexError:
            return
        else:
            id = self.appts[index][0]
            self.curs.execute('DELETE FROM to_do WHERE id=?', (str(id)))

            # update id tags
            self.db_length -= 1
            while id <= self.db_length:
                self.curs.execute('UPDATE to_do SET id=? WHERE id=?', (str(id), str(id + 1)))
                id += 1



            self.db.commit()
            self.refresh_list()
            self.notes_text.delete('0.0', END)
            self.title_entry.delete(0, END)




