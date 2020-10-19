import requests
from pathlib import Path
import json

def get_config():
    config_path = Path(__file__).parent.joinpath('config.json')
    with config_path.open() as config_contents:
        conf = json.load(config_contents)
    return conf


def login(session, login_url, username, password):
    _login = session.get(login_url, allow_redirects=False)
    values = {'user': username, 'pass': password}
    session.cookies = _login.cookies
    session.get(login_url)
    resp = session.post(login_url, data=values, cookies=_login.cookies)
    print(f'[DEBUG] Login response status code{resp.status_code}')
    return session

def get_logged_in_session():
    session = requests.Session()
    config = get_config()
    session = login(session, config['url_login'], config['credentials']['username'], config['credentials']['password'])
    return session