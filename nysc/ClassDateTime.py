from datetime import datetime

class ClassDateTime:

    def __init__(self, class_date_time, current_date_time):
        self.class_date_time = class_date_time
        self.current_date_time = current_date_time

    def within_twelve_hours(self):
        if self.hours_until_class() < 11.75:
            return True

        return False
        
    def todays_date_string(self):
        return datetime.today().strftime('%Y-%m-%d')

    def hours_until_class(self):
        date_format = '%Y-%m-%d %I:%M %p'
        time_difference = abs(self.current_date_time - self.class_date_time)
        hours_difference = time_difference.total_seconds() / 3600.0
        return hours_difference

