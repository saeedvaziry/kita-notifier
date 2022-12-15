from dotenv import load_dotenv
import requests
from bs4 import BeautifulSoup
import os

load_dotenv(".env")


def notify(message: str):
    url = 'https://api.telegram.org/bot%token/sendMessage'.replace('%token', os.environ.get('BOT_TOKEN'))
    requests.post(url, json={
        'chat_id': '89449236',
        'text': 'Kita Navigator: ' + "\n" + message
    })
    print(message)


with requests.Session() as s:
    s.headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_4) AppleWebKit/537.36 (KHTML, like Gecko) '
                      'Chrome/51.0.2704.103 Safari/537.36 '
    }
    token = s.get(os.environ.get('BASE_URL') + '/login/')
    token_soup = BeautifulSoup(token.content.decode('utf-8'), 'html.parser')
    token_el = token_soup.find_all('meta', attrs={'name': 'csrf-token'})
    csrf_token = token_el[0]['content']
    login = s.post(os.environ.get('BASE_URL') + '/login', data={
        'email': os.environ.get('EMAIL'),
        'password': os.environ.get('PASSWORD'),
        '_token': csrf_token
    })
    soup = BeautifulSoup(login.content.decode('utf-8'), 'html.parser')
    table = soup.find_all('i', attrs={'class': 'fal fa-users'})
    msg = ''
    for t in table:
        msg += t.parent.text.strip() + "\n"

    notify(msg)
