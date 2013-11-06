__author__ = 'jibt'

import datetime


def calDate(date):
	date = date.replace("+0800", "")
	dt = datetime.datetime.strptime(date, "%a %b %d %H:%M:%S %Y")
	return dt.strftime("%Y-%m-%d %H:%M:%S")