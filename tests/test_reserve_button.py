import unittest
from datetime import datetime
from nysc.ReserveButton import ReserveButton
from nysc.SportsClubPage import SportsClubPage

class TestReserveButton(unittest.TestCase):

    def setUpWithClassMarkup(self):
        file = open("test_data/class_list_pilates.html", 'r')
        self.parser = SportsClubPage(file.read(), ".toggle-8-17")
        file.close()
        class_time = "8:30 PM"
        class_name = "Pilates Mat"
        return self.parser.get_correct_class_markup(class_name, class_time)

    def setUpWithAtCapacityClass(self):
        file = open("test_data/class_list.html", 'r')
        self.parser = SportsClubPage(file.read(), ".toggle-8-16")
        file.close()
        class_time = "7:30 PM"
        class_name = "Total Body Conditioning"
        return self.parser.get_correct_class_markup(class_name, class_time)        

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

if __name__ == '__main__':
    unittest.main()