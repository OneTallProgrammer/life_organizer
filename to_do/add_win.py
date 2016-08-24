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
        self.notes_label.grid(row=1, sticky='W')

        self.date_label = Label(self.top_frame, text='Date:')
        self.date_label.grid(row=2, sticky='W')

        self.recur_label = Label(self.top_frame, text='Recurrance:')
        self.recur_label.grid(row=3, sticky='W')

        # entries
        self.title_entry = Entry(self.top_frame)
        self.title_entry.grid(row=0, column=1)

        self.date = StringVar()
        self.date.set('Today')
        self.date_entry = Entry(self.top_frame, textvariable=self.date, state='disabled')
        self.date_entry.grid(row=2, column=1)

        self.notes_entry = Entry(self.top_frame)
        self.notes_entry.grid(row=1, column=1)

        # check buttons
        self.checkbox_frame = Frame(self.top_frame, borderwidth=3)
        self.checkbox_frame.grid(row=3, column=1)

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

        self.done_button = Button(self.bottom_frame, text='done', command=master.destroy)
        self.done_button.grid(row=0, column=1, sticky=E)

        '''
            calendar formatting
        '''

        # calendar specific frames

        self.cal_header = Frame(self.cal_frame, bg='white')
        self.cal_header.grid(row=0, column=0)

        self.cal_dates = Frame(self.cal_frame, bg='white')
        self.cal_dates.grid(row=1, column=0)

        self.cal_bottom = Frame(self.cal_frame, bg='white')
        self.cal_bottom.grid(row=2, column=0)

        # buttons
        self.prev = Button(self.cal_header, text='prev', relief=SOLID, bg='white', command=lambda: self.new_month(-1))
        self.prev.grid(row=0, column=0, )

        self.next = Button(self.cal_header, text='next', relief=SOLID, bg='white', command=lambda: self.new_month(1))
        self.next.grid(row=0, column=3)

        # process to generate and manage calendar
        self.today = datetime.date.today()
        self.year = self.today.year
        self.month = self.today.month
        self.pressed_button = Button()
        self.btn_array =[]
        self.cal_data = []

        del self.today

        self.gen_month_data_list()
        self.gen_cal_header()
        self.print_buttons()

        '''
            visual list formatting
        '''
        scrollbar = Scrollbar(self.list_frame)
        scrollbar.grid(row=0, column=1, sticky='NS')

        to_do_list = Listbox(self.list_frame, width=69, yscrollcommand=scrollbar.set)
        to_do_list.grid(row=0, column=0, sticky='E')

        for i in range(1000):
            to_do_list.insert(END, str(i))

        scrollbar.config(command=to_do_list.yview)



        '''
            interactive calendar member functions
        '''

    def gen_month_data_list(self):
        '''
            generates the required data to display calendar information
            @ param self: member function of class Window
        '''
        self.pressed_button = Button()

        text_cal = calendar.TextCalendar()
        month_string = text_cal.formatmonth(self.year, self.month)
        month_list = month_string.split()

        self.cal_data = month_list

    def gen_cal_header(self):
        '''
            generates and displays the month labels at the top of the interactive calendar
            @ param self: member function of class Window
        '''
        self.month_label = Label(self.cal_header, text=self.cal_data[0], bg='white')
        self.month_label.grid(row=0, column=1)

        self.year_label = Label(self.cal_header, text=self.cal_data[1], bg='white')
        self.year_label.grid(row=0, column=2)

    def print_buttons(self):
        '''
            prints a set of interactive buttons corresponding to the date of the month currently selected
            @ param self: member function of class Window
        '''
        self.cal_dates.destroy()
        self.btn_array = []

        self.cal_dates = Frame(self.cal_frame, bg='white')
        self.cal_dates.grid(row=1, column=0)

        grid_width = 7
        start_date_index = 9

        row = 1

        # checks what day of week the first day of the month falls on
        if calendar.weekday(self.year, self.month, 1) == 6:
            column = 0
        else:
            column = calendar.weekday(self.year, self.month, 1) + 1

        index = 2 # start the iterator after the month and year

        while index < start_date_index:
            day_label = Label(self.cal_dates, text=self.cal_data[index], bg='white')
            day_label.grid(row=0, column=index - 2)
            index += 1

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
        '''
            resets all calendar information and generates a new month and displays it
            @ param self: member function of class Window
            @ param mod: int 1 will move the month to the next following month and -1 will move to the previous
        '''
        self.month_label.grid_forget()
        self.year_label.grid_forget()

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
        '''
            button operation that tracks the selected date visually on calendar
            @ param self: member function of class Window
            @ param date: the selected date
        '''
        self.date.set(datetime.date(self.year, self.month, day))
        self.pressed_button['relief'] = FLAT
        self.pressed_button['bg'] = 'white'
        self.btn_array[day - 1]['relief'] = SUNKEN
        self.btn_array[day - 1]['bg'] = 'yellow'
        self.pressed_button = self.btn_array[day - 1]


    def write_to_db(self):
        '''
            writes the users information to the selected database
            @ param self: member function of class Window
        '''

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
        data.append(self.notes_entry.get())
        data.append(self.daily_var.get())
        data.append(self.weekly_var.get())
        data.append(self.monthly_var.get())
        data.append(self.yearly_var.get())

        # write to selected database
        self.curs.execute('INSERT INTO to_do VALUES(?, ?, ?, ?, ?, ?, ? )', (data[0], data[1], data[2], data[3],
                                                                              data[4], data[5], data[6]))
        self.db.commit()

        # clear all fields
        self.title_entry.delete(0, 'end')
        self.date_entry.delete(0, 'end')
        self.notes_entry.delete(0, 'end')
        self.daily_recur.deselect()
        self.weekly_recur.deselect()
        self.monthly_recur.deselect()
        self.yearly_recur.deselect()
