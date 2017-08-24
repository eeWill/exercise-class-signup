from datetime import datetime

class ClassDateTime:

    def __init__(self, class_time):
        self.class_time = class_time

    def within_twelve_hours(self):
        almost_twelve_hours = 11.90
        if self.hours_until_class() < almost_twelve_hours:
            return True

        return False
        
    def todays_date_string(self):
        return datetime.today().strftime('%Y-%m-%d')

    def hours_until_class(self):
        time_difference = abs(datetime.now() - self.class_date_time())
        hours_difference = time_difference.total_seconds() / 3600.0
        return hours_difference

    def class_date_time(self):
        date_format = '%Y-%m-%d %I:%M %p'
        current_date = datetime.today().strftime('%Y-%m-%d')
        return datetime.strptime(current_date + " " + self.class_time, date_format)
    

