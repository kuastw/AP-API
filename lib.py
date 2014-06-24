#-*- coding: utf-8

from bs4 import BeautifulSoup as bs
import requests

session = requests.session()

def login(uid, pwd):
	payload = {
		'pat_submit':'xxx',
		'extpatid':uid,
		'extpatpw':pwd,
		'SUBMIT':'Login',
		'code':'',
		'pin':''
	}
	session.post('http://webopac.lib.kuas.edu.tw/patroninfo', data=payload)
	query()

def query():
	res = bs(session.get('http://webopac.lib.kuas.edu.tw/patroninfo~S0/1109158/readinghistory').text)
	bookname = res.findAll('td', { 'class': 'patFuncTitle'})
	Author = res.findAll('td', { 'class': 'patFuncAuthor'})
	Date = res.findAll('td', { 'class': 'patFuncDate'})
	for i, tag in enumerate(bookname, 0):
		bn = bs(str(bookname[i])).findAll('a')[0].contents[0].encode('utf-8','ignore')
		at = Author[i].contents[0].encode('utf-8','ignore')
		da = Date[i].contents[0].encode('utf-8','ignore')

		print bn + "," + at + "," + da


if __name__ == '__main__':
	login( '1102108132', '')