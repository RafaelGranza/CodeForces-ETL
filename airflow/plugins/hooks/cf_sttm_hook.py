from airflow.hooks.http_hook import HttpHook

import requests
import json
import html
from bs4 import BeautifulSoup


class CfSttmHook(HttpHook):

    def __init__(self, query, conn_id = None):
        self.query = query
        self.conn_id = conn_id or "cf_sttm"
        super().__init__(http_conn_id=self.conn_id)


    def create_url(self):
        query = self.query
        url = f"{self.base_url}/{query}"
        return url


    def get_statments(self, request):
        txt = html.unescape(request.text)
        soup = BeautifulSoup(txt, features="html.parser")
        stm = soup.find("div", class_="problem-statement").find_all("p")
        text = "".join([s.get_text() for s in stm])
        return json.dumps(text)


    def connect_to_endpoint(self, url, session):
        response = requests.Request("GET", url)
        prep = session.prepare_request(response)
        self.log.info(f"URL: {url}")
        return self.get_statments(self.run_and_check(session, prep, {}))


    def run(self):
        session = self.get_conn()
        url = self.create_url()
        return self.connect_to_endpoint(url, session)


if __name__ == "__main__":
    print(json.dumps(CfSttmHook("1614/E").run(), indent=4,sort_keys=True))