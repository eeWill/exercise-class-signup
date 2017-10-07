from bs4 import BeautifulSoup
from nysc import config
from datetime import datetime
from .exceptions.SignupFailed import SignupFailed

class Crawler:

    def __init__(self, client):
        self.client = client

    def login(self, username, password):
        result = self.client.get(config.urls['base_url'] + '/login')
        soup = BeautifulSoup(result.content, 'html.parser')
        csrf_token = soup.find('input', {'name': '_csrf_token'})['value']

        values = {
          '_username': username,
          '_password': password,
          '_csrf_token': csrf_token
        }

        self.client.post(config.urls['base_url'] + '/login_check', data=values)

    def class_filter_url(self, class_type):
        base_url = config.urls['base_url'] + "/classes?"
        club_filter = "club=" + config.nysc["club_name"]
        time_of_day_filter = "&time_of_day=evening"
        category_filter = "&category=" + config.get_category_url_filter(class_type)
        return base_url + club_filter + time_of_day_filter + category_filter

    def attempt_signup_and_check_for_confirmation(self, reserve_link_href):
        result = self.go_to_reserve_url(reserve_link_href)
        try:
            self.parse_confirmation_message(result.content)
        except:
            raise SignupFailed

    def go_to_reserve_url(self, reserve_link_href):
         return self.client.get(self.base_url + '/' + reserve_link_href)

    def parse_confirmation_message(self, html):
        soup = BeautifulSoup(html, 'html.parser')
        confirmation_soup = soup.select_one('.confirmation-header')

        if confirmation_soup is None:
            raise SelectorNotFound()

        return confirmation_soup.text