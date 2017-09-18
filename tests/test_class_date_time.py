import unittest
from datetime import datetime
from nysc.ClassDateTime import ClassDateTime

class TestClassDateTime(unittest.TestCase):

    DATE_FORMAT="%Y-%m-%d %I:%M %p"

    def setUpLessThanTwelveHoursToGo(self):
        class_time = "9:30 AM"
        self.date_time = ClassDateTime(class_time)

    def setUpMoreThanTwelveHoursTillClass(self):
        class_time = "7:30 AM"
        self.date_time = ClassDateTime(class_time)
"""
    def test_less_than_twelve_hours_till_class(self):
        self.setUpLessThanTwelveHoursToGo()
        hours = self.date_time.hours_until_class()
        self.assertLess(hours, 12)

    def test_more_than_twelve_hours_until_class(self):
        self.setUpMoreThanTwelveHoursTillClass()
        hours = self.date_time.hours_until_class()
        self.assertGreater(hours, 12)
"""

if __name__ == '__main__':
    unittest.main()