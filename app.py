import requests
from datetime import datetime, timedelta
from nysc import nysc, config, scheduler
from bs4 import BeautifulSoup
from nysc.SportsClubPage import SportsClubPage
from nysc.ClassDateTime import ClassDateTime
from nysc.ReserveButton import ReserveButton
from nysc.Crawler import Crawler 

client = requests.session()
crawler = Crawler(client)
crawler.login(config.nysc['username'], config.nysc['password'])

selector = ".toggle-%d-%d" % (datetime.now().month, datetime.now().day)

signup = SignupController()
scheduled_class = signup.todays_class()
date_time = ClassDateTime(scheduled_class["time"])

if not signup.already_signed_up() and signup.class_is_scheduled() and date_time.within_twelve_hours():
    classFilterUrl = crawler.classFilterUrl(scheduled_class["name"])
    result = client.get(classFilterUrl)
    page = SportsClubPage(result.content, selector)

    class_markup = page.get_correct_class_markup(requested_class_name, requested_class_time)
    reserve_button = ReserveButton(class_markup)
    reserve_link_href = reserve_button.extract_reserve_url()

    try:
        crawler.attempt_signup_and_check_for_confirmation(reserve_link_href)
        signup.post_successful_signup_attempt()
        print("Signed Up")
    except:
        signup.post_failed_signup_attempt()
        print("Failed Attempt")



# Goal is to remove as many levels of the nesting below as possible.
# More classes and methods may be useful
# Tests and methods for no upcoming classes
# Elses should be eliminated using try catch
# extract_correct_class_if_exists()
# extract_button_href_if_exists()
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