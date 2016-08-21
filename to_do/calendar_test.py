from tkinter import *
import calendar
import datetime

def return_date(day):
    date = datetime.date(2016, 8, int(day))

    return date


c = calendar.TextCalendar(calendar.SUNDAY)
c.setfirstweekday(calendar.SUNDAY)

august = c.formatmonth(2016, 8)

date_list = august.split()

root = Tk()

top_frame = Frame(root)
top_frame.pack()

bottom_frame = Frame(root)
bottom_frame.pack()

month_label = Label(top_frame, text=date_list[0])
month_label.grid(row=0, column=0)

year_label = Label(top_frame, text=date_list[1])
year_label.grid(row=0, column=1)

month = date_list.pop(0)
year = date_list.pop(0)

index = 0
row = 0

#while counter < len(date_list):
for x in range(7):
    wd = Label(bottom_frame, text=date_list[0])
    wd.grid(row=row, column=x)
    date_list.pop(0)

row += 1

if calendar.weekday(int(year), 8, int(date_list[0])) == 6:
    column = 0
else:
    column = calendar.weekday(int(year), 8, int(date_list[0])) + 1

while index < len(date_list):
    new_button = Button(bottom_frame, text=date_list[index], relief=FLAT, command=lambda opt=date_list[index]: print(return_date(int(opt))))
    new_button.grid(row=row, column=column)
    index += 1
    column += 1

    if column > 6:
        column = 0
        row += 1



root.mainloop()

