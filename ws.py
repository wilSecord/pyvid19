import re
import yagmail
import csv
import time
from urllib.request import urlopen
from bs4 import BeautifulSoup
from html.parser import HTMLParser
from datetime import date

today = date.today()
us_url = 'https://www.cdc.gov/coronavirus/2019-ncov/cases-updates/cases-in-us.html'
us_soup = BeautifulSoup(urlopen(us_url), 'html.parser')

l = []
del_spaces = re.compile(r'[1234567890,]+')
callouts = us_soup.select('.callout')

for class_ in callouts:
	cool = class_.get_text()
	c = del_spaces.findall(cool)
	str(cool)
	cool = c
	l.append(cool)

usc = str(l[0][0])
usnc = str(l[0][1])
usd = str(l[1][0])
usnd = str(l[1][1])


def send_email(file):
	global usc
	global usnc
	global usd
	global usnd
	file = open(file, 'a+', newline='')
	writer = csv.writer(file,delimiter='\t')
	writer.writerow([today,usd,usc])
	file.close()
	recipients = ['wilsonsecord@gmail.com']
	body = f'''
		Current US Cases: {usc}
		New US Cases: {usnc}
		CurrentUS Deaths: {usd}
		New US Deaths: {usnd}

		These emails are sent out at 16:30:00 EST
		Any questions? Contact wilsonsecord@gmail.com
		'''

	yag = yagmail.SMTP('pyvid19@gmail.com', r'4x8%zN@msPb!70*v')
	yag.send(
		to=recipients,
		subject='Current COVID-19 Data',
		contents=body,
		attachments='data.csv'
	)

while True:
	time.sleep(86400)
	send_email('data.csv')