import requests
from bs4 import BeautifulSoup

import utilities

session = requests.Session()

def scrape_table(table):
    trs = table.find_all('tr')
    print(trs[0].get_text())

    scores = []
    for item in trs[3:]:
        mediums = item.find_all('td', class_='medium')
        if len(mediums) > 2:
            if mediums[2].get_text() != '-':
                name = item.find_all('td')[0].get_text()
                avg_score = mediums[1].get_text()
                ranking = mediums[2].get_text()
                scores.append({'rank': ranking, 'score': avg_score, 'name': name})

    scores = sorted(scores, key=lambda x: x['rank'])

    for score in scores:
        print(f'{score["rank"]} - avg score {score["score"]} -  {score["name"]}')


def scrape_discipline(score_url):
    s = session.get(score_url)
    soup = BeautifulSoup(s.text, 'html.parser')
    tables = soup.find_all('table')
    for table in tables:
        scrape_table(table)


# Here start the calls
config = utilities.get_config()
session = utilities.get_logged_in_session()
for url in config['urls_scores']:
    scrape_discipline(url)
