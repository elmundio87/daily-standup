import time
from datetime import datetime, date, timedelta


def is_working_day(date):
    return date.weekday() <= 4


def get_working_days(date_start_obj, date_end_obj):

    total_working_days = 0

    date_range = [date_start_obj + timedelta(days=x)
                  for x in range(0, (date_end_obj - date_start_obj).days)]

    for date in date_range:
        if is_working_day(date):
            total_working_days += 1

    return total_working_days
