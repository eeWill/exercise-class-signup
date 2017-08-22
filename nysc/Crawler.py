from bs4 import BeautifulSoup
from nysc import config
from datetime import datetime
from .exceptions.SignupFailed import SignupFailed

class Crawler:

    base_url = 'https://www.newyorksportsclubs.com'
    
    def __init__(self, client):
        self.client = client

    def login(self, username, password):
        result = self.client.get(self.base_url + '/login')
        soup = BeautifulSoup(result.content, 'html.parser')
        csrf_token = soup.find('input', {'name': '_csrf_token'})['value']

        values = {
          '_username': username,
          '_password': password,
          '_csrf_token': csrf_token
        }

        self.client.post(self.base_url + '/login_check', data=values)

    def classFilterUrl(self, class_type):
        today = datetime.today()
        day = str(today.strftime('%d'))
        month = str(today.strftime('%m'))
        baseUrl = self.base_url + "/classes?"
        clubFilter = "class_filter%5Bclub%5D%5B%5D=" + config.class_info["club_id"]
        dateFilter = "&class_filter%5Bday%5D=" + month + "%2F" + day
        timeFilter = "&class_filter%5Btime_of_day%5D%5B%5D=evening"
        classFilter = "&class_filter%5Bcategory%5D%5B%5D=" + config.get_class_type_id_by_string(class_type)
        classFilterUrl = baseUrl + clubFilter + classFilter + dateFilter + timeFilter
        print(classFilterUrl)
        return classFilterUrl

    def attempt_signup_and_check_for_confirmation(self, reserve_link_href):
        result = self.go_to_reserve_url(reserve_link_href)
        try:
            parse_confirmation_message(result.content)
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

