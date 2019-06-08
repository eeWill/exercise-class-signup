import requests
from datetime import datetime, timedelta
from nysc import config
from nysc.SportsClubPage import SportsClubPage
from nysc.ClassDateTime import ClassDateTime
from nysc.ReserveButton import ReserveButton
from nysc.SignupController import SignupController
from nysc.Crawler import Crawler 

signup = SignupController()
scheduled_class = signup.todays_class()
date_time = ClassDateTime(scheduled_class["start_time"])

if not signup.already_signed_up() and signup.class_is_scheduled() and date_time.within_twelve_hours():

    client = requests.session()
    crawler = Crawler(client)
    crawler.login(config.nysc['username'], config.nysc['password'])

    class_filter_url = crawler.class_filter_url(scheduled_class)
    result = client.get(class_filter_url)

    selector = ".toggle-%d-%d" % (datetime.now().month, datetime.now().day)
    page = SportsClubPage(result.content, selector)

    class_markup = page.get_correct_class_markup(scheduled_class)
    reserve_button = ReserveButton(class_markup)
    reserve_link_href = reserve_button.extract_reserve_url()

    try:
        crawler.attempt_signup_and_check_for_confirmation(reserve_link_href)
        signup.post_successful_signup_attempt()
    except:
        signup.post_failed_signup_attempt()