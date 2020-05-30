pyDismail
==============

a pretty basic scraper for yadim.dismail.de, a disposable mail provider

Installation
------------
not on pyPi soo..

    pip install .

Usage
-----


    from pyDismail import Dismail
	
    disposable_mail = Dismail(mail="example")
	print(disposable_mail.mail)
	# example@yadim.dismail.de
	
	mails = Dismail.fetch_all_mails()
	print(mails[0])
	# (Mail Object: 92345, example@gmail.com, datetime.datetime(2020, 5, 25, 12, 12, 12), SUBJECT, CONTENT)
	
	print(mails[0].html_body)
	# <body><p>This is an email</p><p>. Hello</p></body>
	
	print(mails[0].plain_body)
	# This is an email. Hello
	
	disposable_mail.delete_mail(mail[0])
	disposable_mail.check_for_new() # return True if new mail arrived after object created
	disposable_mail.get_eml(mail[0])
	
	
