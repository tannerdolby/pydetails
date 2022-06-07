from src.metadata import PyDetails

def test_get_details():
    page = PyDetails("https://tannerdolby.com")
    doc = page.get_details()
    
    assert doc.get("title").content == "Tanner Dolby"
   