import requests
from datetime import datetime

class SignupController():

    def __init__(self):
        self.current_date = datetime.today().strftime('%Y-%m-%d')

    def get_scheduled_classes(self):
        result = requests.get('https://forte.evwill.com/classes')
        return result.json()["data"]

    def todays_class(self):
        for scheduled_class in self.get_scheduled_classes():
            if scheduled_class["date"] == self.current_date:
                return scheduled_class

    def already_signed_up(self):
        for signup in self.get_signups():
            if signup["date"] == self.current_date and signup["status"] == "Signed Up":
                return True
        
        return False

    def class_is_scheduled(self):
        for scheduled_class in self.get_scheduled_classes():
            if scheduled_class["date"] == self.current_date:
                return True
        
        return False

    def get_signups(self):
        result = requests.get('https://forte.evwill.com/signups')
        return result.json()["data"]

    def post_successful_signup_attempt(self):
        self.post_signup_attempt("Signed Up")

    def post_failed_signup_attempt(self):
        self.post_signup_attempt("Failed Attempt")

    def post_signup_attempt(self, status):
        values = {
            "date": self.current_date,
            "status": status
        }
        result = requests.post('https://forte.evwill.com/signups', data=values)
        
    def get_class_name_by_string(self, class_type):
        if class_type == "Spinning": 
            return "Cycling"
        if class_type == "Conditioning": 
            return "Total Body Conditioning"
        if class_type == "Pilates":
            return "Pilates Mat"
        
        return "Name not found"

    def get_class_time_by_string(self, class_type):
        if class_type == "Spinning": 
            return "7:30 PM"
        if class_type == "Conditioning": 
            return "7:30 PM"
        if class_type == "Pilates":
            return "8:30 PM"
        
        return "Type ID not found"
        