import unittest
from datetime import datetime
from nysc.ReserveButton import ReserveButton
from nysc.SportsClubPage import SportsClubPage

class TestReserveButton(unittest.TestCase):

    def setUpWithClassMarkup(self):
        file = open("tests/fixtures/class_list_pilates.html", 'r')
        self.parser = SportsClubPage(file.read(), ".toggle-8-17")
        file.close()
        scheduled_class = {
            "start_time": "8:30 PM",
            "type": "Pilates Mat"
        }
        return self.parser.get_correct_class_markup(scheduled_class)

    def setUpWithAtCapacityClass(self):
        file = open("tests/fixtures/class_list.html", 'r')
        self.parser = SportsClubPage(file.read(), ".toggle-8-16")
        file.close()
        scheduled_class = {
            "start_time": "7:30 PM",
            "type": "Total Body Conditioning"
        }
        return self.parser.get_correct_class_markup(scheduled_class)        

    def test_if_reserve_button_exists(self):
        class_markup = self.setUpWithClassMarkup()
        reserve_button = ReserveButton(class_markup)
        self.assertTrue(reserve_button.exists())

    def test_get_text_from_reserve_button(self):
        class_markup = self.setUpWithClassMarkup()
        reserve_button = ReserveButton(class_markup)
        self.assertEqual(reserve_button.text(), "Reserve")

    def test_get_text_from_at_capacity_button(self):
        class_markup = self.setUpWithAtCapacityClass()
        reserve_button = ReserveButton(class_markup)
        self.assertEqual(reserve_button.text(), "At capacity")

    def test_extract_reserve_url_from_button(self):
        signup_url = "/classes/19637559/reserve"
        class_markup = self.setUpWithClassMarkup()
        reserve_button = ReserveButton(class_markup)
        self.assertEqual(reserve_button.extract_reserve_url(), signup_url)
        

if __name__ == '__main__':
    unittest.main()