#!/usr/bin/python

import subprocess, sys, datetime, pwd, os, calendar, itertools, ConfigParser

workday_count = 5
valid_days = list(calendar.day_abbr)[:workday_count]


def load_config():
    config = ConfigParser.SafeConfigParser()
    config.read('config.ini')

    return config


def get_input():
    arg_names = ['command','day']
    args = dict(itertools.izip_longest(arg_names, sys.argv))

    day = args['day']
    if day is None:
        sys.exit("Please specify home office day!")
    elif day not in valid_days:
        sys.exit("You must provide one of the following days: ["+",".join(valid_days)+"]")
    else:
        return day


def calculate_date(home_office_day):
    now = datetime.datetime.now()
    first_day_in_week = now - datetime.timedelta(days=now.weekday())
    dates = {}

    for d in range(now.weekday(), workday_count):
        day = (first_day_in_week + datetime.timedelta(days=d))
        day_name = day.strftime("%a")
        full_name = day.strftime("%A, %d %b %Y")
        dates[day_name] = full_name

    chosen_day = dates.get(home_office_day)
    if chosen_day is None:
        sys.exit("You cannot select past days")
    else:
        return chosen_day


def prepare_message(date, author):
    message_file = open('message.html')
    message = message_file.read()
    return message.replace('$DATE', date).replace('$AUTHOR', author)


# TODO: look into SMTP
def send_message(recipient, subject, body):
    try:
        process = subprocess.Popen(['mail', '-s', subject, recipient], stdin=subprocess.PIPE)
    except Exception, error:
        print error
    process.communicate(body)


def get_name():
    # TODO: use config as a fallback?
    name = pwd.getpwuid(os.getuid())[4].split(", ")
    return name[1] + " " + name[0]


def format_my_email(email):
    return get_name() + "<" + email + ">"


def main():
    config = load_config()
    day = get_input()

    try:
        recipient = config.get("email", "recipient")
        sender = config.get("email", "sender")
    except (ConfigParser.NoOptionError, ConfigParser.NoSectionError) as e:
        sys.exit("Invalid configuration file!")


    date = calculate_date(day)
    subject = 'Home Office Request for ' + date + '\nContent-Type: text/html\nFrom: ' + format_my_email(sender)
    author = get_name()
    body = prepare_message(date, author)

    send_message(recipient, subject, body)

main()