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
    s.get(os.environ.get('BASE_URL') + '/login/')
    login = s.post(os.environ.get('BASE_URL') + '/login/', data={
        'str_email': os.environ.get('EMAIL'),
        'str_passwort': os.environ.get('PASSWORD'),
        'act_login': '',
    })
    kitas = s.get(os.environ.get('BASE_URL') + '/login/startseite/')
    soup = BeautifulSoup(kitas.content.decode('utf-8'), 'html.parser')
    table = soup.find_all('table', attrs={'class': 'contenttable stackable'})
    match = False
    msg = ''
    for t in table:
        rows = t.findChildren('tr')
        for r in rows:
            columns = r.findChildren('td')
            for i, c in enumerate(columns):
                if i == 1:
                    value = "".join(line.strip() for line in c.string.split("\n"))
                    msg += value + "\n"

    notify(msg)
