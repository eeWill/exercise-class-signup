from bs4 import BeautifulSoup
from .exceptions.SelectorNotFound import SelectorNotFound

class SportsClubPage:

    def __init__(self, html, row_selector):
        self.soup = BeautifulSoup(html, 'html.parser')
        self.row_selector = row_selector

    def parse_classes_table_markup(self):
        return self.soup.select(self.row_selector)

    def get_correct_class_markup(self, scheduled_class):
        for class_markup in self.parse_classes_table_markup():
            if scheduled_class["type"] == self.extract_class_name_from_markup(class_markup) and scheduled_class["start_time"] == self.extract_start_time_from_markup(class_markup):
                return class_markup

    def extract_start_time_from_markup(self, class_markup):
        class_time_markup = class_markup.select_one(".big")
        split_parsed_time = class_time_markup.text.split(' - ')
        return split_parsed_time[0]

    def extract_class_name_from_markup(self, class_markup):
        class_name_markup = class_markup.select_one(".bigger")
        return class_name_markup.text.replace("\n", "").strip();

    def extract_reserve_url(self, class_markup):
        reserve_button = class_markup.select_one(".reserve")
        return reserve_button.get('href')

