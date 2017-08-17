import unittest
from nysc.SportsClubPage import SportsClubPage
from nysc.exceptions.SelectorNotFound import SelectorNotFound

class TestSportsClubPage(unittest.TestCase):

    def setUpWithConfirmationPage(self):
        file = open("test_data/successful_signup.html", 'r')
        self.parser = SportsClubPage(file.read(), ".toggle-8-16")
        file.close()

    def setUpWithLittleMarkup(self):
        self.parser = SportsClubPage("<div>This is just a little bit of markup</div>", ".toggle-8-16")

    def setUpWithClassList(self):
        file = open("test_data/class_list.html", 'r')
        self.parser = SportsClubPage(file.read(), ".toggle-8-16")
        file.close()

    def test_parse_confirmation_page(self):
        self.setUpWithConfirmationPage()
        confirmation_markup = self.parser.parse_confirmation_message()
        self.assertTrue("You have a spot" in confirmation_markup)

    def test_parse_time_markup_with_non_confirmation_page(self):
        self.setUpWithLittleMarkup()
        self.assertRaises(SelectorNotFound, self.parser.parse_confirmation_message)

    def test_parse_table_markup_selection_returns_an_array(self):
        self.setUpWithClassList()
        length_of_markup_array = len(self.parser.parse_classes_table_markup())
        self.assertTrue(length_of_markup_array > 0)

    def test_get_correct_class_markup_returns_string(self):
        self.setUpWithClassList()
        correct_class = self.parser.get_correct_class_markup("Cycling", "6:30 AM")
        self.assertTrue(isinstance(correct_class, str))

    def test_extract_start_time_from_markup_returns_correct_time(self):
        self.setUpWithClassList()
        single_class = self.parser.parse_classes_table_markup()[0]
        class_time = self.parser.extract_start_time_from_markup(single_class)
        self.assertEqual(class_time, "6:30 AM")

    def test_extract_class_name_from_markup_returns_cycling(self):
        self.setUpWithClassList()
        single_class = self.parser.parse_classes_table_markup()[0]
        class_name = self.parser.extract_class_name_from_markup(single_class)
        self.assertEqual(class_name, "Cycling")

    def test_get_correct_class_markup_by_config(self):
        self.setUpWithClassList()
        class_time = "6:30 AM"
        class_name = "Cycling"
        class_markup = self.parser.get_correct_class_markup(class_name, class_time)
        self.assertTrue(class_time in class_markup)
        self.assertTrue(class_name in class_markup)

    def test_get_correct_class_by_config_conditioning_at_730(self):
        self.setUpWithClassList()
        class_time = "7:30 PM"
        class_name = "Total Body Conditioning"
        class_markup = self.parser.get_correct_class_markup(class_name, class_time)
        self.assertTrue(class_time in class_markup)
        self.assertTrue(class_name in class_markup)

if __name__ == '__main__':
    unittest.main()