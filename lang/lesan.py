#unoffical translation api for lesan.ai

import json
import requests
from fake_useragent import UserAgent

class Lesan:
    url = "https://lesan.ai/translate-text"
    def __init__(self,text:str,user_agent: UserAgent | str = UserAgent(min_version=120.0))-> None:
        self.user_agent = user_agent if type(user_agent) is str else user_agent.random
        self.headers = {
                "Accept-Language":"en-US,en;q=0.9,am;q=0.8,fa;q=0.7",
                "Content-Type": "application/json",
                "Cookie": "session=eyJjc3JmX3Rva2VuIjoiYjdkNDJmYTZmNDgxNWZkMjAyOGMwY2NhNjI5NTFlMWNkNDMwMDYzNSJ9.Zp-R_w.p4Bvn9ltYXgTNoISOxkbyr5Z2oc; _gid=GA1.2.1562549859.1721733635; _ga_417FF2NZCC=GS1.1.1721741964.12.0.1721741964.60.0.0; _ga=GA1.2.1377139705.1717078791; _gat_gtag_UA_141462480_1=1",
                "Host": "lesan.ai",
                "Origin": "https://lesan.ai",
                "Referer": "https://lesan.ai/",
        }
        self.text = text

        #source langues ["am", "en", "ti"]

    #decoder
    def __decoder(self,response):
        decoded_response = json.loads(response.text)
        translated_text = decoded_response[0]["text"]
        return translated_text
    
    def translate(self, destination:str="am") -> str:
        self.payload = {
            "text":f"{self.text}",
            "src_lang":"auto",
            "tgt_lang":f"{destination}"
        }

        return self.__sendRequest()
    
    def __sendRequest(self):
        response = requests.post(Lesan.url, headers=self.headers,json=self.payload)
        if response.status_code == 200:
            try:
                translated = self.__decoder(response)
                return translated
            except json.JSONDecodeError as e:
                print("Error decoding JSON:",e)

        else:
            print("Error:",response.status_code, response.reason)



q1 = Lesan("do you love animals")
print(q1.translate("am"))