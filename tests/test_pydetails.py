from src.pydetails import PyDetails
import unittest

class TestPyDetails(unittest.TestCase):
    # TODO: test the output and potentially process some HTML for more meaningful assertions
    def test_twitter_card(self):
        card_type = "twitter_summary"
        page = PyDetails("https://tannerdolby.com", card_type)
        doc = page.get_details()
        card = page.build_card()

        self.assertEqual(doc.get("title").content, "Tanner Dolby")
        self.assertEqual(doc.get("description").content, "Hi, I'm Tanner. A software engineer and mathematician with a passion for building things for the web.")
        self.assertNotEqual(card, "")
   
if __name__ == '__main__':
    unittest.main()
