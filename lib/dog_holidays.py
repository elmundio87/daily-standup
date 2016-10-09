import holidays
from datetime import date
from dateutil.relativedelta import relativedelta as rd
from dateutil.rrule import rrule, DAILY


class DevOpsGuysHolidays(holidays.UnitedKingdom):
    def _populate(self, year):

        excluded_holidays = [
            "St. Patrick's Day",
            "St. Patrick's Day (Observed)"
        ]

        # Populate the holiday list with the default UK holidays
        holidays.UnitedKingdom._populate(self, year)

        for holiday, name in self.items():
            if name in excluded_holidays:
                self.pop(holiday, None)

        xmas_holidays_start = date(year, 12, 25)
        xmas_holidays_end = date(year, 12, 31)

        for holiday in rrule(DAILY, dtstart=xmas_holidays_start, until=xmas_holidays_end):
            if holiday not in self:
                self[holiday] = "Office Closed for Christmas"
