
from scraper import scraper
from requests import Session

if __name__ == '__main__':
    print('\nStarting....\n')
    session = Session()
    scraper(session)