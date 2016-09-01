from tkinter import *
import datetime
import calendar

class Window:
    def __init__(self, master, db, curs):
        master.title('Add a To Do Item')
        master.resizable(width=False, height=False)
        master.minsize(width=550, height=380)

        #link the window to the db
        self.db = db
        self.curs = curs

        '''
            general layout formatting
        '''

        # main frames
        self.entry_frame = Frame(master)
        self.entry_frame.grid(row=0, column=0, sticky='NW')

        self.cal_frame = Frame(master, borderwidth=10, height=225, width=325, bg='white')
        self.cal_frame.grid(row=0, column=1)
        self.cal_frame.grid_propagate(False)

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

        self.daily_var = IntVar()
        self.daily_recur = Checkbutton(self.checkbox_frame, text='dy', variable=self.daily_var)
        self.daily_recur.grid(row=0, column=0)
        self.daily_recur.config(highlightbackground='white')

        self.weekly_var = IntVar()
        self.weekly_recur = Checkbutton(self.checkbox_frame, text='wk', variable=self.weekly_var)
        self.weekly_recur.grid(row=0, column=1)
        self.weekly_recur.config(highlightbackground='white')

        self.monthly_var = IntVar()
        self.monthly_recur = Checkbutton(self.checkbox_frame, text='mn', variable=self.monthly_var)
        self.monthly_recur.grid(row=0, column=2)
        self.monthly_recur.config(highlightbackground='white')

        self.yearly_var = IntVar()
        self.yearly_recur = Checkbutton(self.checkbox_frame, text='yr', variable=self.yearly_var)
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

        self.to_do_list.bind("<ButtonRelease-1>", self.display_notes)



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

        string = string.replace('\n', '')
        string = string.replace('\t', '')

        return string

    def refresh_list(self):
        WEEK = 7

        # clear the list
        self.to_do_list.delete(0, END)

        # select daily recurring appointments
        self.curs.execute('SELECT title, date, d, w, m, y FROM to_do WHERE date=? OR d=? OR w=? OR m=? OR y=?',
                          (self.date.get(),1, 1, 1, 1))

        for row in self.curs.fetchall():
            if row[2] == 1:
                # daily recurrence
                title = row[0]
                self.to_do_list.insert(END, title)
                self.to_do_list.itemconfig(END, bg='#99ff99')
            elif row[3] == 1 or row[4] == 1 or row[5] == 1:
                date_made = datetime.datetime.strptime(row[1], "%Y-%m-%d")
                date_selected = datetime.datetime.strptime(self.date.get(), "%Y-%m-%d")

                # weekly recurrence
                if (date_selected - date_made).days % WEEK == 0 and row[3] == 1:
                    title = row[0]
                    self.to_do_list.insert(END, title)
                    self.to_do_list.itemconfig(END, bg='#ccccff')

                # monthly/yearly recurrence
                elif row[4] == 1 or row[5] == 1:
                    # date made variables
                    year_1 = date_made.year
                    month_1 = date_made.month
                    day_1 = date_made.day

                    # date selected variables
                    year_2 = date_selected.year
                    month_2 = date_selected.month
                    day_2 = date_selected.day

                    # monthly recurrence
                    end_of_month = calendar.monthrange(year_2, month_2)[1]
                    if day_2 == end_of_month and day_1 > end_of_month:
                        day_2 = day_1
                    if day_1 == day_2 and row[4] == 1:
                        title = row[0]
                        self.to_do_list.insert(END, title)
                        self.to_do_list.itemconfig(END, bg='#ffcc66')

                    # yearly recurrence
                    elif (month_1 == month_2 and day_1 == day_2) and row[5] == 1:
                        title = row[0]
                        self.to_do_list.insert(END, title)
                        self.to_do_list.itemconfig(END, bg='#66ccff')

            elif row[2] == 0 and row[3] == 0 and row[4] == 0 and row[5] == 0 and row[1] == self.date.get():
                    title = row[0]
                    self.to_do_list.insert(END, title)

    def display_notes(self, click):
        try:
            index = self.to_do_list.curselection()[0]
        except IndexError:
            return
        else:
            # clear the title and notes entries
            self.title_entry.delete(0, END)
            self.notes_text.delete('0.0', END)

            # select the notes with the proper title and date
            self.curs.execute("SELECT title, notes FROM to_do WHERE title=?", (self.to_do_list.get(index),))
            # extract the string
            selection = self.curs.fetchall()
            selection = selection[0]
            title = selection[0]
            notes = selection[1]

            # print to the notes' and title fields
            self.title_entry.insert(0, title)
            self.notes_text.insert('0.0', notes)

    def write_to_db(self):
        """
            writes the users information to the selected database
            @ param self: member function of class Window
        """

        # if there is no title, assume the user has not entered it correctly
        if self.title_entry.get() == '':
            return

        data = []

        # load data into tuple
        if self.date.get() == 'Today': # entry field defaults to today's date
            data.append(datetime.date.today())
        else:
            data.append(self.date.get())


        data.append(self.title_entry.get())
        data.append(self.notes_text.get('1.0', END))
        data.append(self.daily_var.get())
        data.append(self.weekly_var.get())
        data.append(self.monthly_var.get())
        data.append(self.yearly_var.get())

        # remove outer spaces
        data[1] = self.format_string(data[1])
        data[2] = self.format_string(data[2])

        # Delete any duplicate before writing
        self.curs.execute('DELETE FROM to_do WHERE date=? AND title=?', (data[0], data[1]))




        # write to selected database
        self.curs.execute('INSERT INTO to_do VALUES(?, ?, ?, ?, ?, ?, ? )', (data[0], data[1], data[2], data[3],
                                                                              data[4], data[5], data[6]))
        self.db.commit()

        # clear all fields
        self.title_entry.delete(0, 'end')
        self.date_entry.delete(0, 'end')
        self.notes_text.delete('1.0', END)
        self.daily_recur.deselect()
        self.weekly_recur.deselect()
        self.monthly_recur.deselect()
        self.yearly_recur.deselect()

        self.refresh_list()

    def remove_from_db(self):
        try:
            index = self.to_do_list.curselection()[0]
        except IndexError:
            return
        else:
            self.curs.execute('DELETE FROM to_do WHERE title=?', (self.to_do_list.get(index),))
            self.db.commit()
            self.refresh_list()
            self.notes_text.delete('0.0', END)
            self.title_entry.delete(0, END)