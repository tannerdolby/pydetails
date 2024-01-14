from src.pydetails import PyDetails

def main():
    page = PyDetails('https://tannerdolby.com')
    print(page.build_card())

main()