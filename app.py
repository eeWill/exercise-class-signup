import requests
from datetime import datetime, timedelta
from nysc import nysc, config, scheduler
from epoch import epoch
from bs4 import BeautifulSoup

client = requests.session()
crawler = nysc.Crawler(config.nysc['username'], config.nysc['password'], client)
crawler.login() 

def is_correct_class(soup, config, class_type):
    parsed_time = soup.select('.cell-head .big')[0].text
    split_parsed_time = parsed_time.split(' - ')
    start_time = split_parsed_time[0]
    parsed_class_name = soup.select('.cell-md-left .bigger')[0].text
    if config.get_class_time_by_string(class_type) in start_time and config.get_class_name_by_string(class_type) in parsed_class_name:
        return True
    
    return False

def todays_class(classes, current_date):
    for scheduled_class in classes:
        if scheduled_class["date"] == current_date:
            return scheduled_class
    
    return False

### Check if we are within 12 hours of class
current_date = datetime.today().strftime('%Y-%m-%d')

already_signed_up = False
if scheduler.already_signed_up(current_date, client):
    already_signed_up = True

classes = scheduler.get_scheduled_classes(client)
todays_class = todays_class(classes, current_date)
date_format = '%Y-%m-%d %I:%M %p'

if todays_class is not False:
    class_start_time = config.get_class_time_by_string(todays_class["type"])
    class_date_time = datetime.strptime(current_date + " " + class_start_time, date_format)
    hours_difference = epoch.hours_difference(datetime.today(), class_date_time)

#If there is a class scheduled, and we're within 11.75 hours of it
if not already_signed_up and todays_class and hours_difference < 11.75:
    classFilterUrl = crawler.classFilterUrl(todays_class["type"])
    classes = client.get(classFilterUrl)
    soup = BeautifulSoup(classes.content, 'html.parser')

    #Loop through the found classes, if the time and type is correct, mimic a link click!
    if is_correct_class(soup, config, todays_class["type"]):
        reserve_button = soup.select('.reserve')
        #Click reserve button if it exists, otherwise post the status to database
        if reserve_button: 
            reserve_href = soup.select('.reserve')[0]['href']
            signup = client.get('https://www.newyorksportsclubs.com' + reserve_href)
            # Check if signed up, then run the below code, if still not signed up, print/enter that in the database
            # h1.confirmation-header check for "You have a spot"
            status_text = "Signed Up"
            scheduler.post_signup_attempt(current_date, status_text, client)
        else:
            button_text = soup.select('.disabled')[0].text
            scheduler.post_signup_attempt(current_date, button_text, client)
            print("Class status is currently: " + button_text)
    else:
        print("Wasn't able to determine if this is the correct class.")
else: 
    print("No class scheduled for today or already signed up.")
    