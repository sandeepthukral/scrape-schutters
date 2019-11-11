import json
import requests
from bs4 import BeautifulSoup
from pathlib import Path

login_url = 'https://www.flevoschutters.nl/competitie/login/'
score_urls = [
        'https://www.flevoschutters.nl/competitie/get-score/discipline/1',
        'https://www.flevoschutters.nl/competitie/get-score/discipline/2',
        'https://www.flevoschutters.nl/competitie/get-score/discipline/3',
        'https://www.flevoschutters.nl/competitie/get-score/discipline/19'
        ]

session = requests.Session()


def get_config():
    config_path = Path(__file__).parent.joinpath('config.json')
    with config_path.open() as config_contents:
        conf = json.load(config_contents)
    return conf


def login(username, password):
    _login = session.get(login_url, allow_redirects=False)
    values = {'user': username, 'pass': password}
    session.cookies = _login.cookies
    session.get(login_url)
    session.post(login_url, data=values, cookies=_login.cookies)


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


def scrape_discipline(url):
    s = session.get(url)
    soup = BeautifulSoup(s.text, 'html.parser')
    tables = soup.find_all('table')
    for table in tables:
        scrape_table(table)


# Here start the calls
config = get_config()
login(config['credentials']['username'], config['credentials']['password'])
for score_url in score_urls:
    scrape_discipline(score_url)
