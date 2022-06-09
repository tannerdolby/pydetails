from src.metadata import PyDetails

# TODO: test the output and potentially process some HTML for more meaningful assertions
def test_twitter_card():
    page = PyDetails("https://tannerdolby.com")
    card = page.build_card("twitter", page.get_details())

    assert card != ""
