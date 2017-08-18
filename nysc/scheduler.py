from datetime import datetime

def get_scheduled_classes(client):
    result = client.get('https://forte.evwill.com/classes')
    return result.json()["data"]

def get_signups(client):
    result = client.get('https://forte.evwill.com/signups')
    return result.json()["data"]

def post_signup_attempt(date, status, client):
    values = {
      "date": date,
      "status": status
    }
    result = client.post('https://forte.evwill.com/signups', data=values)

def already_signed_up(date, client):
    for signup in get_signups(client):
        if signup["date"] == date and signup["status"] == "Signed Up":
            return True
    
    return False

def todays_class(client):
    current_date = datetime.today().strftime('%Y-%m-%d')
    for scheduled_class in get_scheduled_classes(client):
        if scheduled_class["date"] == current_date:
            return scheduled_class

def class_is_scheduled(client):
    current_date = datetime.today().strftime('%Y-%m-%d')
    for scheduled_class in get_scheduled_classes(client):
        if scheduled_class["date"] == current_date:
            return True
    
    return False

