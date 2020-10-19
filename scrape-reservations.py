import requests
from bs4 import BeautifulSoup
import utilities

ignore_texts = [
    "19:30", "20:00", "20:30", "21:00", "21:30", "22:00", 
    "11:00: Squad 1", "11:00: Squad 2", "11:00: Squad 3",
    "19:30: Squad 1", "19:30: Squad 2", "19:30: Squad 3"
    "14:30 ", "15:00", "15:30", "16:00", "16:30",
    "Niet beschikbaar", "Reserveer als BC", "Reserveren", "Gereserveerd voor instroom !!BC!!", "Wacht op BC", "Niet in gebruik"
]

def scrape_page(url):
    session = utilities.get_logged_in_session()
    s = session.get(url)
    soup = BeautifulSoup(s.text, 'html.parser')

    names = []

    tables = soup.find_all('table')
    for table in tables:
        tds = table.find_all('td')

        for td in tds:
            td_text = td.get_text()
            if td_text in ignore_texts:
                continue
            else :
                if ":" in td_text or td_text == '':
                    continue
                if td_text not in names:
                    names.append(td_text)

    return sorted(names)

# Here start the calls
config = utilities.get_config()
all_names = scrape_page(config['url_reservation'])
print('The following users are registered to shoot')
for name in all_names:
    print(name)