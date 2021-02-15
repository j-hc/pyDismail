import requests
import string
import random
import re
from eml_parser import EmlParser
from datetime import datetime


class _Mail:
    def __init__(self, mail_id, sender, time, subject, body, parsed_eml):
        self.parsed_eml: dict = parsed_eml
        self.mail_id: int = mail_id
        self.sender: str = sender
        self.subject: str = subject
        self.body: str = body
        self.time: datetime = time

        if len(self.body) > 30:
            self._truncated_body = f"{self.body[:30]}..."
        else:
            self._truncated_body = self.body

    def __repr__(self):
        return '(Mail: sender={}, time={}, subject={}, id={}, body={})'\
            .format(self.sender, self.time, self.subject, self.mail_id, self._truncated_body)


class Dismail:
    _req_obj = requests.Session()
    _base_url = "https://yadim.dismail.de"
    _re_mail_id = re.compile(b'id="mail-box-(.*?)"')

    def __init__(self, mail: str = None, fetch_on_start: bool = True, eml_parser_kwargs: dict = {'include_raw_body': True}):
        self._eml_parser = EmlParser(**eml_parser_kwargs)
        if mail is None:
            self.mail = self._get_random()
        if mail.endswith('@yadim.dismail.de'):
            self.mail = mail
        else:
            self.mail = f"{mail}@yadim.dismail.de"
        self._mail_url = f"{self._base_url}/?{self.mail}"
        self.all_mails = []

        self._mails_recvd = []
        if fetch_on_start:
            self.fetch_all_mails()

    def _get_random(self):
        return self._req_obj.get(self._base_url).url.split('?')[1]

    def check_for_new(self) -> int:
        params = {
            'action': 'has_new_messages',
            'address': self.mail,
            'email_ids': '|'.join(self._mails_recvd)
        }
        response = self._req_obj.get(self._base_url, params=params)
        return int(response.text)

    def fetch_all_mails(self) -> list:
        mail_ids = self._fetch_ids()
        for mail_id in reversed(mail_ids):
            if mail_id in self._mails_recvd:
                continue
            raw_eml = self._get_eml_by_id(mail_id)
            parsed_eml = self._eml_parser.decode_email_bytes(raw_eml)
            body = parsed_eml['body'][0]['content']
            sender = parsed_eml['header']['from']
            time = parsed_eml['header']['date']
            subject = parsed_eml['header']['subject']
            self.all_mails.append(_Mail(mail_id, sender, time, subject, body, parsed_eml))
            self._mails_recvd.append(mail_id)
        return self.all_mails

    def get_eml(self, mail: _Mail) -> bytes:
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
        response = self._req_obj.get(self._mail_url)
        return [mail_id.decode() for mail_id in self._re_mail_id.findall(response.content)]

    def delete_mail(self, mail: _Mail) -> None:
        params = {
            'action': 'delete_email',
            'email_id': mail.mail_id,
            'address': self.mail
        }
        self._req_obj.get(self._base_url, params=params)
