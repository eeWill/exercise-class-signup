from nysc import config

def hours_difference(date_one, date_two):
	time_difference = abs(date_one - date_two)
	hours_difference = time_difference.total_seconds() / 3600.0
	return hours_difference

