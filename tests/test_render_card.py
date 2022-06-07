from src.metadata import PyDetails

def test_twitter_card():
    page = PyDetails("https://tannerdolby.com")
    card = page.render_card("twitter", page.get_details())

    assert card != ""
