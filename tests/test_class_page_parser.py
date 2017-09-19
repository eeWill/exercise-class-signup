import unittest
from nysc.SportsClubPage import SportsClubPage
from nysc.exceptions.SelectorNotFound import SelectorNotFound

class TestSportsClubPage(unittest.TestCase):

    def setUpWithConfirmationPage(self):
        file = open("tests/fixtures/successful_signup.html", 'r')
        self.parser = SportsClubPage(file.read(), ".toggle-8-16")
        file.close()

    def setUpWithLittleMarkup(self):
        self.parser = SportsClubPage("<div>This is just a little bit of markup</div>", ".toggle-8-16")

    def setUpWithClassList(self):
        file = open("tests/fixtures/class_list.html", 'r')
        self.parser = SportsClubPage(file.read(), ".toggle-8-16")
        file.close()

    def setUpWithClassListJustPilates(self):
        file = open("tests/fixtures/class_list_pilates.html", 'r')
        self.parser = SportsClubPage(file.read(), ".toggle-8-17")
        file.close()

    def test_parse_table_markup_selection_returns_an_array(self):
        self.setUpWithClassList()
        length_of_markup_array = len(self.parser.parse_classes_table_markup())
        self.assertTrue(length_of_markup_array > 0)

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
        class_time= "6:30 AM"
        class_name = "Cycling"
        scheduled_class = {
            "start_time": class_time,
            "type": class_name
        }
        class_markup = self.parser.get_correct_class_markup(scheduled_class)
        self.assertTrue(class_time in class_markup.text)
        self.assertTrue(class_name in class_markup.text)

    def test_get_correct_class_by_config_conditioning_at_730(self):
        self.setUpWithClassList()
        class_time = "7:30 PM"
        class_name = "Total Body Conditioning"
        scheduled_class = {
            "start_time": class_time,
            "type": class_name
        }
        class_markup = self.parser.get_correct_class_markup(scheduled_class)
        self.assertTrue(class_time in class_markup.text)
        self.assertTrue(class_name in class_markup.text)


if __name__ == '__main__':
    unittest.main()