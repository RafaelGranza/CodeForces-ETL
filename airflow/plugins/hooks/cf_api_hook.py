from airflow.hooks.http_hook import HttpHook

import requests
import json
# from urllib.request import urlopen
# from bs4 import BeautifulSoup


class CfApiHook(HttpHook):

    def __init__(self, query, conn_id = None):
        self.query = query
        self.conn_id = conn_id or "cf_airflow"
        super().__init__(http_conn_id=self.conn_id)


    def create_url(self, **kwargs):
        query = self.query
        url = f"{self.base_url}/{query}?"
        for k, arg in kwargs.items():
            url += f"{k}={arg}&"
        return url[:-1]


    def connect_to_endpoint(self, url, session):
        response = requests.Request("GET", url)
        prep = session.prepare_request(response)
        self.log.info(f"URL: {url}")
        return self.run_and_check(session, prep, {}).json()


    # def get_statments(self, contestId=1614, index="E"):
    #     url = f"https://codeforces.com/problemset/problem/{contestId}/{index}"
    #     html = urlopen(url).read()
    #     soup = BeautifulSoup(html, features="html.parser")
    #     stm = soup.find("div", class_="problem-statement").find_all("p")
    #     text = "".join([s.get_text() for s in stm])
    #     return text


    def run(self, get_statment=False):        
        session = self.get_conn()
        url = self.create_url()
        return self.connect_to_endpoint(url, session)


if __name__ == "__main__":
    print(json.dumps(CfApiHook("contest.list?gym=true").run(), indent=4,sort_keys=True))