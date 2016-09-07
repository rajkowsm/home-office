#!/usr/bin/python

import subprocess, sys, datetime, pwd, os

def calculate_date(homeOfficeDay):
	workdays=5
	now = datetime.datetime.now()
	first_day_in_week = now - datetime.timedelta(days=now.weekday())
	dates = {}

	for d in range(now.weekday(),workdays):
		day=(first_day_in_week + datetime.timedelta(days=d+7))
		dayName=day.strftime("%a")
		fullDate=day.strftime("%A, %d %b %Y")
		dates[dayName]=fullDate

	chosenDay=dates.get(homeOfficeDay)
	if chosenDay == None:
		sys.exit('You cannot select past days!')
	else:
		return chosenDay

def prepare_message(date, author):
	file = open('message.html')
	message = file.read()
	return message.replace('$DATE', date).replace('$AUTHOR', author)

# TODO: look into SMTP
def send_message(recipient, subject, body):
    try:
      process = subprocess.Popen(['mail', '-s', subject, recipient], stdin=subprocess.PIPE)
    except Exception, error:
      print error
    process.communicate(body)

def get_name():
	name=pwd.getpwuid(os.getuid())[4].split(", ")
	return name[1]+" "+name[0]

recipient = sys.argv[1]
homeOfficeDay=sys.argv[2]

subject = 'Home Office Request\nContent-Type: text/html'

author=get_name()
date=calculate_date(homeOfficeDay)
body=prepare_message(date, author)

send_message(recipient, subject, body)