from src.metadata import PyDetails

page = PyDetails("https://tannerdolby.com")

def test_twitter_card():
    card = page.render_card("twitter", page.get_details())

    assert card != ""
