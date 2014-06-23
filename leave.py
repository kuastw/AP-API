#-*- encoding=utf-8

from bs4 import BeautifulSoup as bs
import requests

session = requests.session()

def login( uid, pwd):
	res = bs(session.get( 'http://leave.kuas.edu.tw/' ).text)
	form = {}
	for i in res.findAll('input'):
		form[i['name']] = i['value'] if i.get('value') != None else ""
	form['Login1$UserName'] = uid
	form['Login1$Password'] = pwd
	session.post( 'http://leave.kuas.edu.tw/', data=form )

def getList():
	res = bs(session.get( 'http://leave.kuas.edu.tw/AK002MainM.aspx').text)
	form = {}
	for i in res.findAll('input'):
		form[i['name']] = i['value']
	form['ctl00$ContentPlaceHolder1$SYS001$DropDownListYms'] = '102-2'
	res = bs(session.post( 'http://leave.kuas.edu.tw/AK002MainM.aspx', data=form ).text)
	table = res.findAll('table', { 'id': 'ContentPlaceHolder1_AK002_GridViewDaily'})
	for i in bs(str(table[0])).findAll('tr'):
		s = ""
		for td in bs(str(i)).findAll('td'):
			s += td.contents[0].encode('utf-8','ignore').replace(' ','') + ","
		print s

if __name__ == '__main__':
	login( '', '')
	getList()