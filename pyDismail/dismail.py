import requests
import string
from bs4 import BeautifulSoup
import random
import datetime


class _mailObj:
    def __init__(self, id_, sender, time, title, body):
        self.id_ = id_
        self.sender = sender
        self.title = title
        self.plain_body = self._plain_builder(body)
        self.html_body = body
        self.time = time

    def __repr__(self):
        return '(Mail Object: {}, {}, {}, {}, {})'.format(self.id_, self.sender, self.time, self.title, self.plain_body.encode())

    def _plain_builder(self, body):
        text = ""
        for txt in body.findAll(text=True, recursive=True):
            text += txt.strip()
        return text


class Dismail:
    __req_obj = requests.Session()
    __base_url = "https://yadim.dismail.de/"

    def __init__(self, mail="random", fetch_on_start=False):
        if mail == "random":
            self.mail = self.getRandom()
        if '@yadim.dismail.de' in mail:
            self.mail = mail
        else:
            self.mail = mail + "@yadim.dismail.de"
        if fetch_on_start:
            self.__mails_recvd = self.__fetch_ids()
        else:
            self.__mails_recvd = None
        
    def __getRandom(size=6, chars=string.ascii_lowercase + string.digits):
        base = ''.join(random.choice(chars) for _ in range(size))
        return base + "@yadim.dismail.de"

    def check_for_new(self):
        params = (
            ('action', 'has_new_messages'),
            ('address', self.mail),
            ('email_ids', self.__mails_recvd),
        )
        response = self.__req_obj.get(self.__base_url, params=params)
        resp_decoded = response.content.decode()
        if str(resp_decoded) == "0":
            return False
        else:
            self.__mails_recvd = self.__fetch_ids()
            return True

    def fetch_all_mails(self):
        response = self.__req_obj.get('{0}?{1}'.format(self.__base_url, self.mail))
        main_page = BeautifulSoup(response.content, "lxml")
        status = main_page.find('div', id="email-list")

        mailObjs = []
        first_tags = []
        second_tags = []
        for header_tag in status.find_all('a', class_='list-group-item list-group-item-action email-list-item'):
            id_ = header_tag["href"].split("-")[2]
            sender = header_tag.find('span').text
            title = header_tag.find('p').text.strip()
            time = header_tag.find('small').get("title")
            date_time_obj = datetime.datetime.strptime(time, '%Y-%m-%d %H:%M:%S')
            first_tags.append([id_, sender, date_time_obj, title])
        for body_tag in status.find_all('div', class_='card-block email-body'):
            for not_needed in body_tag.find_all('div', class_="float-right primary"):
                not_needed.extract()
            second_tags.append(body_tag)

        for i in range(0, len(first_tags)):
            first_tags[i].append(second_tags[i])
            mailObjs.append(_mailObj(*first_tags[i]))
        return mailObjs

    def get_eml(self, mailObj):
        params = (
            ('action', 'download_email'),
            ('email_id', mailObj.id_),
            ('address', self.mail),
        )
        response = requests.get(self.__base_url, params=params)
        return response.content

    def __fetch_ids(self):
        response = self.__req_obj.get('{0}/?{1}'.format(self.__base_url, self.mail))
        soup = BeautifulSoup(response.content, "lxml")
        status = soup.find_all('a', class_='list-group-item list-group-item-action email-list-item')
        ids = []
        for stat in status:
            ids.append(stat["href"].split("-")[2])
        return "|".join(ids)

    def delete_mail(self, mailObj):
        params = (
            ('action', 'delete_email'),
            ('email_id', mailObj.id_),
            ('address', self.mail),
        )
        self.__req_obj.get(self.__base_url, params=params)

