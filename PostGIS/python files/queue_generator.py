import random
from datetime import datetime
import calendar


def to_hour(ihour, iminute):
    return round(ihour + iminute / 60, 2)


def busy_gen():
    today = datetime.now()
    year, month, day = today.year, today.month, today.day
    # hour, minute = today.hour, today.minute
    last = calendar.monthrange(year, month)[1]
    payday = [1, 10, 20, last]
    current_hour = to_hour(today.hour, today.minute)
    day_of_week = today.isoweekday()
    busy = 0

    if day in payday:
        busy += 1
    if 17.5 <= current_hour < 22:
        busy += 1
    if day_of_week > 5:
        busy += 1
    else:
        if 12 <= current_hour < 14:
            busy += 1
    return busy


def queue_gen(busy):
    if busy <= 0:
        return random.randint(0, 3)
    if busy == 1:
        return random.randint(0, 4)
    if busy == 2:
        return random.randint(0, 5)
    if busy >= 3:
        return random.randint(1, 5)
