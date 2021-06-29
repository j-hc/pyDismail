import requests
import re
from eml_parser import EmlParser
from datetime import datetime
from typing import List


__all__ = ['YadimDismail', 'BmOn2Dismail', 'BlubbermailDismail']


class Mail:
    def __init__(self, mail_id, sender, time, subject, body, parsed_eml):
        self.parsed_eml: dict = parsed_eml
        self.mail_id: int = mail_id
        self.sender: str = sender
        self.subject: str = subject
        self.body: str = body
        self.time: datetime = time

    @property
    def truncated_body(self):
        if len(self.body) > 30:
            return f"{self.body[:30]}..."
        else:
            return self.body

    def __repr__(self):
        return '(Mail: sender={}, time={}, subject={}, id={}, body={})'\
            .format(self.sender, self.time, self.subject, self.mail_id, self.truncated_body)


class Dismail:
    _base_url = None
    _base_url_api = None
    _domain = None
    __req_session = requests.Session()
    # __re_mail_id = re.compile(b'id="mail-box-(.*?)"')
    __re_mail_id = re.compile(b'email_ids=(.*?)"')

    def __init__(self, mail: str = None, eml_parser_kwargs: dict = None):
        if eml_parser_kwargs is None:
            eml_parser_kwargs = {}
        eml_parser_kwargs.update({'include_raw_body': True})

        self._eml_parser = EmlParser(**eml_parser_kwargs)
        if mail is None:
            self.mail = self._get_random()
        elif mail.endswith(f"@{self._domain}"):
            self.mail = mail
        else:
            self.mail = f"{mail}@{self._domain}"
        self._mail_url = f"{self._base_url}/?{self.mail}"
        self._mail_ids_recvd = []

    def _get_random(self):
        params = {
            'action': 'random'
        }
        return self.__req_session.get(self._base_url, params=params).headers['location'][1:]

    def check_for_new(self) -> int:
        params = {
            'action': 'has_new_messages',
            'address': self.mail,
            'email_ids': '|'.join(self._mail_ids_recvd)
        }
        response = self.__req_session.get(self._base_url_api, params=params)
        return int(response.text)

    def fetch_all_mails(self) -> List[Mail]:
        mails = []
        mail_ids = self._fetch_ids()
        for mail_id in reversed(mail_ids):
            if mail_id in self._mail_ids_recvd:
                continue
            raw_eml = self._get_eml_by_id(mail_id)
            parsed_eml = self._eml_parser.decode_email_bytes(raw_eml)
            body = parsed_eml['body'][0]['content']
            sender = parsed_eml['header']['from']
            time = parsed_eml['header']['date']
            subject = parsed_eml['header']['subject']
            mails.append(Mail(mail_id, sender, time, subject, body, parsed_eml))
            self._mail_ids_recvd.append(mail_id)
        return mails

    def get_eml(self, mail: Mail) -> bytes:
        return self._get_eml_by_id(mail.mail_id)

    def _get_eml_by_id(self, mail_id):
        params = {
            'action': 'download_email',
            'email_id': mail_id,
            'address': self.mail
        }
        response = requests.get(self._base_url, params=params)
        return response.content

    def _fetch_ids(self):
        response = self.__req_session.get(self._mail_url)
        emailids = self.__re_mail_id.search(response.content).group(1)
        if bool(emailids):
            return emailids.decode('utf-8').split('|')
        else:
            return []

    def delete_mail(self, mail: Mail) -> None:
        params = {
            'action': 'delete_email',
            'email_id': mail.mail_id,
            'address': self.mail
        }
        self.__req_session.get(self._base_url, params=params)


class YadimDismail(Dismail):
    def __init__(self, mail: str = None, eml_parser_kwargs: dict = None):
        self._base_url = "https://yadim.dismail.de"
        self._base_url_api = "https://yadim.dismail.de"
        self._domain = "yadim.dismail.de"
        super().__init__(mail, eml_parser_kwargs)


class BmOn2Dismail(Dismail):
    def __init__(self, mail: str = None, eml_parser_kwargs: dict = None):
        self._base_url = "https://www.bm.on2.de"
        self._base_url_api = "https://www.bm.on2.de/json-api.php"
        self._domain = "bm.on2.de"
        super().__init__(mail, eml_parser_kwargs)


class BlubbermailDismail(Dismail):
    def __init__(self, mail: str = None, eml_parser_kwargs: dict = None):
        self._base_url = "https://blubbermail.de"
        self._base_url_api = "https://blubbermail.de/json-api.php"
        self._domain = "blubbermail.de"
        super().__init__(mail, eml_parser_kwargs)
