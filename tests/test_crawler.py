import unittest
from datetime import datetime
from nysc.Crawler import Crawler
from nysc.SportsClubPage import SportsClubPage
from nysc.exceptions.SelectorNotFound import SelectorNotFound
from nysc.exceptions.SignupFailed import SignupFailed
class TestCrawler(unittest.TestCase):

    def setUpWithConfirmationPage(self):
        file = open("test_data/successful_signup.html", 'r')
        self.crawler = Crawler(file.read())
        file.close()

    def confirmation_html(self):
        file = open("test_data/successful_signup.html", 'r') 
        html = file.read()
        file.close()
        return html

    def setUpWithLittleMarkup(self):
        self.crawler = Crawler("<div>This is just a little bit of markup</div>")
    
    def test_attempt_signup_and_check_for_confirmation_without_confirmation(self):
        self.setUpWithLittleMarkup()
        reserve_url = "/classes/19637559/reserve"
        self.assertRaises(SignupFailed, self.crawler.attempt_signup_and_check_for_confirmation(reserve_url))
    
    def test_attempt_signup_and_check_for_confirmation(self):
        self.setUpWithConfirmationPage()
        html = self.confirmation_html()
        confirmation_markup = self.crawler.parse_confirmation_message(html)
        self.assertTrue("You have a spot" in confirmation_markup)

    def test_parse_time_markup_with_non_confirmation_page(self):
        self.setUpWithLittleMarkup()
        html = self.confirmation_html()
        self.assertRaises(SelectorNotFound, self.crawler.parse_confirmation_message(html))