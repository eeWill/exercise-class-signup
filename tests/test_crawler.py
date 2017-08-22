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

    def setUpWithLittleMarkup(self):
        self.crawler = Crawler("<div>This is just a little bit of markup</div>")
    
    def test_attempt_signup_and_check_for_confirmation_without_confirmation(self):
        self.setUpWithLittleMarkup()
        self.assertRaises(SignupFailed, self.crawler.attempt_signup_and_check_for_confirmation())
    
    def test_attempt_signup_and_check_for_confirmation(self):
        self.setUpWithConfirmationPage()
        confirmation_markup = self.crawler.parse_confirmation_message()
        self.assertTrue("You have a spot" in confirmation_markup)

    def test_parse_time_markup_with_non_confirmation_page(self):
        self.setUpWithLittleMarkup()
        self.assertRaises(SelectorNotFound, self.crawler.parse_confirmation_message)