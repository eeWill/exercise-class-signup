# Exercise Class Signup

Python web crawler that signs up for class if a spot opens up. It makes heavy use of the BeautifulSoup parsing library.

## How it works
1. Makes a call to an endpoint on an AWS server to determine if the user wants to signup for class today. It also checks if a signup has already occured today.
1. If it is determined that a signup attempt should occur, the crawler logs in and accesses the class page on the gym website.
1. It parses the page to find the class, and attempts to signup by navigating to the reservation url if it's found.
1. Logs the attempt as a success or failure by making a POST to the AWS server.

Since classes are often full, this project runs on a frequent cronjob for the best chances of signing up.

## Remote server
- Laravel install running on an EC2 instance and a RDS MySQL database.
- Some basic endpoints exist for logging attempts and getting the list of currently scheduled classes.
