import requests
from urllib.request import urlopen
from bs4 import BeautifulSoup

def get_problems():
    r = requests.get('https://codeforces.com/api/problemset.problems?tags=implementation')
    print(r.json())

def get_statments(contestId=1614, index='E'):
    url = f'https://codeforces.com/problemset/problem/{contestId}/{index}'
    html = urlopen(url).read()
    soup = BeautifulSoup(html, features="html.parser")
    stm = soup.find("div", class_="problem-statement").find_all("p")
    text = "".join([s.get_text() for s in stm])
    return text

get_statments()