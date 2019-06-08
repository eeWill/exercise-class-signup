from bs4 import BeautifulSoup

class ReserveButton():

    def __init__(self, class_markup):
        self.class_markup = class_markup

    def exists(self):
        return self.get_button() != None
        
    def text(self):
        return self.get_button().text

    def extract_reserve_url(self):
        return self.get_button().get("href")

    def get_button(self):
        return self.class_markup.select_one('.cell-foot > .button-wrapper > a.reserve')
