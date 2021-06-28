pyDismail
==============

an API wrapper for yadim.dismail.de, a disposable mail provider

Installation
------------
not on pyPi soo..
    
    git clone https://github.com/scrubjay55/pyDismail
    pip3 install ./pyDismail


Usage
```python
from pyDismail import Dismail

disposable_mail = Dismail(mail="example", fetch_on_start=False) # if mail is left None, a random one will be assigned
print(disposable_mail.mail)
# example@yadim.dismail.de

mails = disposable_mail.fetch_all_mails()
last_received_mail = mails[-1]
print(last_received_mail)
# (Mail: sender=SENDER, time=DATETIME, subject=SUBJECT, id=ID, body=BODY)

print(last_received_mail.parsed_eml)
# parsed eml of the email

print(last_received_mail.body)  # plain body of the email
# This is an email. Hello

disposable_mail.delete_mail(last_received_mail)
# deletes the mail from the server, though still can be read from disposable_mail.all_mails

is_there_new_mail = disposable_mail.check_for_new()
# returns the amount of the new mails after the last fetch_all_mails was called

disposable_mail.get_eml(last_received_mail)
# returns the raw eml content of the email
```