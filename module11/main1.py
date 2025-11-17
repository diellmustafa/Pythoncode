import datetime

example1 = datetime.datetime.now()
print("Year:", example1.year)
print("Month:", example1.month)
print("Day:", example1.day)
print("Hour:", example1.hour)
print("Minute:", example1.minute)
print("Second:", example1.second)
print("Microsecond:", example1.microsecond)

newdate = example1 + datetime.timedelta(days = 100)
print(newdate)
olddate = example1 + datetime.timedelta(days = -100)
print(olddate)

sept = datetime.datetime(2024, 9, 1, 8, 0, 0, 0)

with open('formatted_dates.txt', 'w') as file:
    file.write(str(sept))