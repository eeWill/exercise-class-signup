from bs4 import BeautifulSoup

class SportsClubPage:

    def __init__(self, html):
        self.soup = BeautifulSoup(html, 'html.parser')

    def parse_start_time_markup(self):
        return 1

    def extract_start_time_from_markup(self):
        return 1

    def parse_class_name(self):
        return 1

    def parse_confirmation_message(self):
        confirmation_soup = self.soup.select('.confirmation-header')
        return self.soup.select('.confirmation-header')