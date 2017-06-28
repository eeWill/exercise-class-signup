# NYSC Signup

Python web crawler that signs up for NYSC classes.

## Introduction
This project is meant to run on a frequent cronjob. On each run an Amazon RDS database is queried to see if any classes are scheduled for today. 

If the current time is within 12 hours, the user is not already signed up, and the class is not at capacity, the crawler goes to the reservation link which signs the user up for the class.