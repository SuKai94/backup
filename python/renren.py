#!usr/bin/env/python
#coding: utf-8
import urllib
import urllib2
import cookielib
import hashlib
from bs4 import BeautifulSoup

import sys
reload(sys)
sys.setdefaultencoding('utf-8')

class renren(object):

	def __init__(self, email, passwd):
		self.email = email
		self.passwd = passwd
		self.cookie = cookielib.CookieJar()
		self.opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(self.cookie))
		self.headers = {
			'User-Agent':
				'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Ubuntu Chromium/28.0.1500.52 Chrome/28.0.1500.52 Safari/537.36'
		}
		self.login_url = 'http://www.renren.com/PLogin.do'
		self.response = None
		self.content = None
		self.soup = None

	def login(self):
		data = {
			'email': self.email,
			'password': self.passwd
		}
		post_data = urllib.urlencode(data)
		req = urllib2.Request(url=self.login_url, data=post_data, headers=self.headers)
		self.response = self.opener.open(req)
		self.content = self.response.read()
		self.soup = BeautifulSoup(self.content)

	def recent_visit(self):
		visits = []
		all_rencent_visit = self.soup.findAll('span', {'class': 'tip-content'})
		for one_visit in all_rencent_visit:
			t = one_visit.get_text()
			visits.append(t)
		visits[0] = '最近来访:'
		return visits

	def today_birthday(self):
		today_birthdays = []
		all_today_birth = self.soup.findAll('a', {'class': 'uname'})
		for one_birth in all_today_birth:
			t = one_birth.get_text()
			today_birthdays.append(t)
		return today_birthdays

	def close(self):
		self.opener.close()

def main():
	sk_renren = renren('your email here', 'your password here')
	sk_renren.login()

	visits = sk_renren.recent_visit()
	for visit in visits:
		print visit

	birthdays = sk_renren.today_birthday()
	print '\n今天过生日的有：'
	for birth in birthdays:
		print birth 

	sk_renren.close()


if __name__ == '__main__':
	main()