import unittest
import working_days
from datetime import date


class TestWorkingDays(unittest.TestCase):

    def test_monday_is_working_day(self):
        self.assertTrue(working_days.is_working_day(date(2016, 10, 3)))

    def test_tuesday_is_working_day(self):
        self.assertTrue(working_days.is_working_day(date(2016, 10, 4)))

    def test_wednesday_is_working_day(self):
        self.assertTrue(working_days.is_working_day(date(2016, 10, 5)))

    def test_thursday_is_working_day(self):
        self.assertTrue(working_days.is_working_day(date(2016, 10, 6)))

    def test_friday_is_working_day(self):
        self.assertTrue(working_days.is_working_day(date(2016, 10, 7)))

    def test_saturday_is_not_working_day(self):
        self.assertFalse(working_days.is_working_day(date(2016, 10, 8)))

    def test_sunday_is_not_working_day(self):
        self.assertFalse(working_days.is_working_day(date(2016, 10, 9)))

    def test_there_are_zero_working_days_between_saturday_and_sunday(self):
        saturday = date(2016, 10, 8)
        sunday = date(2016, 10, 9)
        self.assertEqual(working_days.get_working_days(saturday, sunday), 0)

    def test_there_is_one_working_day_between_friday_and_the_following_monday(self):
        friday = date(2016, 10, 7)
        following_monday = date(2016, 10, 10)
        self.assertEqual(working_days.get_working_days(friday, following_monday), 1)

    def test_return_zero_if_the_second_date_is_in_the_past(self):
        friday = date(2016, 10, 7)
        last_monday = date(2016, 10, 3)
        self.assertEqual(working_days.get_working_days(friday, last_monday), 0)

    def test_new_years_bank_holiday_is_not_working_day(self):
        self.assertTrue(working_days.is_working_day(date(2017, 2, 1)))

if __name__ == '__main__':
    suite = unittest.TestLoader().loadTestsFromTestCase(TestWorkingDays)
    unittest.TextTestRunner(verbosity=0).run(suite)
