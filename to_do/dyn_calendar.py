from tkinter import *
import calendar
import datetime

global selection
selection = 'Today'

class interactive_calendar:
    def __init__(self, year, month):
        self.master = Tk()
        self.master.title('CALENDER')
        self.master.minsize(width=310, height=0)
        self.master.resizable(width=False, height=False)

        self.btn_array = [] #holds all of the button objects used for dates
        self.pressed_button = Button(self.master)

        self.year = year
        self.month = month

        #self.data_list = self.generate_month_list(self.year, self.month)

        self.not_done = True # set to False when user is ready to exit calendar

        self.header_frame = Frame(self.master)
        self.header_frame.grid(row=0, column=0)

        self.date_frame = Frame(self.master)
        self.date_frame.grid(row=1, column=0)

        self.display_date_frame = Frame(self.master)
        self.display_date_frame.grid(row=2, column=0)

        self.date = StringVar()
        self.date.set('Today')

        self.add_button = Button(self.display_date_frame, text='add', command=
        lambda: set_selection(self.date.get()))
        self.add_button.grid(row=0, column=0)

        self.done_button = Button(self.display_date_frame, text='done', command=
        lambda: self.master.destroy())
        self.done_button.grid(row=0, column=1)

        # heading lablels
        self.year_label = Label(self.header_frame, text='')
        self.month_label = Label(self.header_frame, text='')

        # next and prev buttons scroll through the months
        self.prev = Button(self.header_frame, text='prev', relief=SOLID, command=lambda: self.new_month(-1))
        self.prev.grid(row=0, column=0, sticky='w')

        self.next = Button(self.header_frame, text='next', relief=SOLID, command=lambda: self.new_month(1))
        self.next.grid(row=0, column=3)

        # opens calender to the current month
        self.new_month(0)

        self.master.mainloop()

    def return_date(self):
        return self.date.get()

    def new_month(self, mod):
        self.month_label.grid_forget()
        self.year_label.grid_forget()

        self.month += mod

        if self.month == 13:
            self.year += 1
            self.month = 1
        elif self.month == 0:
            self.year -= 1
            self.month =  12

        self.data_list = self.generate_month_list(self.year, self.month)

        self.month_label = Label(self.header_frame, text=self.data_list[0])
        self.month_label.grid(row=0, column=1)

        self.year_label = Label(self.header_frame, text=self.data_list[1])
        self.year_label.grid(row=0, column=2)

        self.print_buttons()

    def print_buttons(self):
        self.date_frame.destroy()

        self.date_frame = Frame(self.master)
        self.date_frame.grid(row=1, column=0)

        grid_width = 7
        start_date_index = 9

        row = 1


        if calendar.weekday(self.year, self.month, 1) == 6:
            column = 0
        else:
            column = calendar.weekday(self.year, self.month, 1) + 1

        index = 2

        while index < start_date_index:
            day_label = Label(self.date_frame, text=self.data_list[index])
            day_label.grid(row=0, column=index - 2)
            index += 1
        self.btn_array = []
        #print the dates as buttons and bind them to a method
        while index < len(self.data_list):
            new_button = Button(self.date_frame, text=self.data_list[index], relief=FLAT, command=
            lambda opt=int(self.data_list[index]):
            self.select_day(opt, self.btn_array)
            )

            self.btn_array.append(new_button)

            new_button.grid(row=row, column=column)

            index += 1
            column += 1

            if column == grid_width:
                column = 0
                row += 1

    def select_day(self, day, day_list):
        self.date.set(datetime.date(self.year, self.month, day))
        day_list[day - 1]['relief'] = SUNKEN
        self.pressed_button['relief'] = FLAT
        self.pressed_button = day_list[day - 1]

    def generate_month_data_list(self):
        text_cal = calendar.TextCalendar()
        month_string = text_cal.formatmonth(self.year, self.month)
        month_list = month_string.split()

        return month_list

    def gen_header(self, data_list):
        self.month_label = Label(self.header_frame, text=data_list[0])
        self.month_label.grid(row=0, column=1)

        self.year_label = Label(self.header_frame, text=data_list[1])
        self.year_label.grid(row=0, column=2)

    def generate_month_list(self, year, month):
        cal = calendar.TextCalendar()
        month_string = cal.formatmonth(year, month)
        month_list = month_string.split()
        #print(month_list)
        return month_list

def set_selection(date):
    global selection
    selection = date
    print(selection)

def open_calendar():
    global selction

    # generate today
    today = datetime.date.today()

    # extract month and year
    year = int(today.year)
    month = int(today.month)

    # today object holds no other purpose
    del today


    # generate interactive calendar
    cal = interactive_calendar(year, month)

    print(selection)
    return selection




