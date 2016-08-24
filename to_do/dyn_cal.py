from tkinter import *

class interactive_calendar:
    def __init__(self, year, month):
        self.master = Tk()
        self.master.title('CALENDER')
        self.master.minsize(width=310, height=0)
        self.master.resizable(width=False, height=False)

        self.selection = 'Today'

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

        self.add_button = Button(self.display_date_frame, text='add', command=
        lambda: set_selection(self.date.get()))
        self.add_button.grid(row=0, column=0)

        self.done_button = Button(self.display_date_frame, text='done', command=
        lambda: self.exit_window())
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
