import unittest
import app

class TestStringMethods(unittest.TestCase):

    def test_in_string(self):
        website_date_string = '7:30 PM - 8:15 PM'
        start_time = '7:30'
        split_website_date_string = website_date_string.split(' - ')
        self.assertTrue(app.in_string(start_time, split_website_date_string[0]))

        website_class_name = 'Cycling'
        class_name = 'Cycling'
        self.assertTrue(app.in_string(website_class_name, class_name))
        self.assertFalse(app.in_string(website_class_name, 'Body Conditioning'))

        

if __name__ == '__main__':
    unittest.main()