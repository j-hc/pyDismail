import requests
import string
from bs4 import BeautifulSoup
import random
import datetime


class _mailObj:
    def __init__(self, id, sender, time, title, body):
        self.id = id
        self.sender = sender
        self.title = title
        self.body = body
        self.time = time

    def __repr__(self):
        return '(Mail Object: {}, {}, {}, {}, {})'.format(self.id, self.sender, self.time, self.title, self.body.encode())


class Dismail:
    __req_obj = requests.Session()
    __base_url = "https://yadim.dismail.de/"

    def __init__(self, mail="random"):
        if mail == "random":
            self.mail = self.getRandom()
        if '@yadim.dismail.de' in mail:
            self.mail = mail
        else:
            self.mail = mail + "@yadim.dismail.de"
        self.__mails_recvd = self.__fetch_ids()
        
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
            id = header_tag["href"].split("-")[2]
            sender = header_tag.find('span').text
            title = header_tag.find('p').text.strip()
            time = header_tag.find('small').get("title")
            date_time_obj = datetime.datetime.strptime(time, '%Y-%m-%d %H:%M:%S')
            first_tags.append([id, sender, date_time_obj, title])
        for body_tag in status.find_all('div', class_='card-block email-body'):
            for not_needed in body_tag.find_all('div'):
                not_needed.extract()
            second_tags.append(body_tag.text.strip())

        for i in range(0, len(first_tags)):
            first_tags[i].append(second_tags[i])
            mailObjs.append(_mailObj(*first_tags[i]))
        return mailObjs

    def __fetch_ids(self):
        response = self.__req_obj.get('{0}/?{1}'.format(self.__base_url, self.mail))
        soup = BeautifulSoup(response.content, "lxml")
        status = soup.find_all('a', class_='list-group-item list-group-item-action email-list-item')
        ids = []
        for stat in status:
            ids.append(stat["href"].split("-")[2])
        return "|".join(ids)

    def delete_by_id(self, id):
        params = (
            ('action', 'delete_email'),
            ('email_id', str(id)),
            ('address', self.mail),
        )
        self.__req_obj.get(self.__base_url, params=params)
