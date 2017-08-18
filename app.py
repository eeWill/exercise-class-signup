import requests
from datetime import datetime, timedelta
from nysc import nysc, config, scheduler
from bs4 import BeautifulSoup
from nysc.SportsClubPage import SportsClubPage
from nysc.ClassDateTime import ClassDateTime

client = requests.session()
crawler = nysc.Crawler(config.nysc['username'], config.nysc['password'], client)
crawler.login() 



current_date_time = datetime.now()
selector = ".toggle-%d-%d" % (current_date_time.month, current_date_time.day)
current_date = datetime.today().strftime('%Y-%m-%d')

todays_requested_class = scheduler.todays_class(client)
already_signed_up = scheduler.already_signed_up(current_date, client)

requested_class_time = config.get_class_time_by_string(todays_requested_class["type"])
requested_class_name = config.get_class_name_by_string(todays_requested_class["type"])

date_format = '%Y-%m-%d %I:%M %p'
class_date_time = datetime.strptime(current_date + " " + requested_class_time, date_format)
date_time = ClassDateTime(current_date_time, class_date_time)

if not already_signed_up and scheduler.class_is_scheduled(client) and date_time.within_twelve_hours():
    classFilterUrl = crawler.classFilterUrl(todays_requested_class["type"])
    result = client.get(classFilterUrl)
    page = SportsClubPage(result.content, selector)

    class_markup = page.get_correct_class_markup(requested_class_name, requested_class_time)
    reserve_url = page.extract_reserve_url(class_markup)
    print(class_markup.text)
    print(reserve_url)

# Goal is to remove as many levels of the nesting below as possible.
# More classes and methods may be useful
# Tests and methods for no upcoming classes

"""

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
    """