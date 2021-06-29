pyDismail
==============

an API wrapper for temporary/disposable mail providers powered by [synox/disposable-mailbox](https://github.com/synox/disposable-mailbox)

Installation
------------
not on pyPi soo..

    pip install git+git://github.com/scrubjay55/pyDismail@master


Usage
```python
from pyDismail import BlubbermailDismail, BmOn2Dismail, YadimDismail


disposable_mail = BlubbermailDismail(mail="example")  # or BmOn2Dismail(mail="example")
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
# deletes the mail from the server

amount_of_new_mail = disposable_mail.check_for_new()
print(amount_of_new_mail)
# returns the amount of the new mails after the last fetch_all_mails was called

raw_eml = disposable_mail.get_eml(last_received_mail)
# returns the raw eml content of the email

```