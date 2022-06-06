from src.metadata import PyDetails

page = PyDetails("https://tannerdolby.com")

def test_get_details():
    doc = page.get_details()
    print(doc)
    pass
   