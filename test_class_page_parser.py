import unittest
from nysc.SportsClubPage import SportsClubPage

class TestSportsClubPage(unittest.TestCase):

    def setUpWithConfirmationPage(self):
        file = open("test_data/successful_signup.html", 'r')
        self.parser = SportsClubPage(file.read())
        file.close()

    def setUpWithLittleMarkup(self):
        self.parser = SportsClubPage("<div>This is just a little bit of markup</div>")

    def test_parse_confirmation_page(self):
        self.setUpWithConfirmationPage()
        confirmation_markup = self.parser.parse_confirmation_message()
        self.assertTrue("You have a spot" in confirmation_markup)

    def test_parse_time_markup_with_non_confirmation_page(self):
        self.setUpWithLittleMarkup()
        confirmation_markup = self.parser.parse_confirmation_message()
        self.assertRaises(IndexError, confirmation_markup)

if __name__ == '__main__':
    unittest.main()