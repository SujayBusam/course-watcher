import requests
from bs4 import BeautifulSoup
import re
import smtplib
import time
from email.MIMEMultipart import MIMEMultipart
from email.MIMEText import MIMEText

CLASS_YEAR = "2008"
MAX_ENR = 300

def main():
	# Class data
	url = "http://oracle-www.dartmouth.edu/dart/groucho/timetable.course_quicksearch"
	# subject = raw_input("Enter class subject (4 letter code in lowercase): " )
	# course_num = raw_input("Enter course number: " )
	subject = "cosc"
	course_num = "65"
	post_data = {
		"classyear": CLASS_YEAR,
		"subj": subject,
		"crsenum": course_num
	}

	is_class_open = False

	url_data = scrape_url(url, post_data)

	from_addr = 'FordPrefect064@gmail.com'
	# pwd = raw_input("Enter email password: ")
	pwd = "barktreehouse"
	to_addr  = 'sujay.busam@gmail.com'
	phone_addr = '7245701827@mms.att.net'


	while not is_class_open:
		class_data = parse_url(url_data, subject)
		if class_data[1] < class_data[0]:
			send_mail(from_addr, pwd, to_addr, subject, course_num)
			send_text(from_addr, pwd, phone_addr, subject, course_num)
			print "messages sent"
			is_class_open = True
		time.sleep(30)


def scrape_url(url, post_data):
	r = requests.post(url, data = post_data)
	return r.text

def parse_url(url_data, subject):
	soup = BeautifulSoup(url_data)

	# print soup.prettify()

	text = subject.upper()
	
	# Get the table cell that holds course subject
	subj_cell = soup.find_all('td', text=re.compile(text))
	subj_cell = subj_cell[1].parent

	# Get "Lim" cell
	lim_cell = subj_cell.parent
	for i in range(14):
		lim_cell = lim_cell.find_next('td')

	# Enrollment number cell
	enr_cell = lim_cell.find_next('td')

	# Enrollment limit
	try:
		enr_limit = int(lim_cell.contents[0])
	except:
		enr_limit = MAX_ENR
	
	# Current enrollment
	curr_enr = int(enr_cell.contents[0])

	class_data = [enr_limit, curr_enr]
	return class_data

def start_server(from_addr, pwd):
	server = smtplib.SMTP('smtp.gmail.com', 587)
	server.ehlo()
	server.starttls()
	server.ehlo()
	server.login(from_addr, pwd)

	return server

def send_mail(from_addr, pwd, to_addr, subject, course_num):
	# Email header
	msg = MIMEMultipart()
	msg['From'] = from_addr
	msg['To'] = to_addr
	msg['Subject'] = "Class available"

	# Email body
	body = subject.upper() + " " + course_num + " " + "is available!"
	msg.attach(MIMEText(body, 'plain'))

	server = start_server(from_addr, pwd)
	text = msg.as_string()
	server.sendmail(from_addr, to_addr, text)

def send_text(from_addr, pwd, to_addr, subject, course_num):
	# Text body
	body = subject.upper() + " " + course_num + " " + "is available!"

	server = start_server(from_addr, pwd)
	server.sendmail("Joe", to_addr, body)

# Standard boilerplate to call the main() function to begin
# the program.
if __name__ == '__main__':
    main()