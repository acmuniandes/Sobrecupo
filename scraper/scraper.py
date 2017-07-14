import os
import requests
from bs4 import BeautifulSoup

BASE_URL = "https://registroapps.uniandes.edu.co/"
USER_AGENT = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.95 Safari/537.36"
EXTRA_SCHEDULE = 26

def scrape():

    mainPage = request("https://registroapps.uniandes.edu.co/scripts/adm_con_horario_19_joomla.php")

    depSoup = BeautifulSoup(mainPage, 'html5lib')

    for link in depSoup.find_all('a', href = True):
        scrapeDep(link)

def scrapeDep(depTag):

    #Stores the url from the tag
    depHTML = depTag['href']

    print("Entering: " + depHTML)

    if isRelative(depHTML):
        depHTML = BASE_URL + depHTML[2:-1]

    depPage = request(depHTML)

    depSoup = BeautifulSoup(depPage, 'html5lib')

    for tableTag in depSoup.find_all('table', cellspacing="1"):
        extractTables(tableTag)

def isRelative(url):
    return url.startswith('..')

def extractTables(tableTag):
    descendants = len(list(tableTag.descendants))
    if matchSchedule(descendants):
        try:
            print (tableTag.find('font', class_ ='texto4').string + ' desc = ' + str(descendants))
        except Exception as error:
            print (error)
    elif descendants >= 77 and descendants < 370:
        try:
            print(tableTag.find_all(encontrarTitulo)[0].string.lstrip().rstrip())
        except Exception as error:
            print(str(error) + " desc = " + str(descendants) + " - 47 = " + str(descendants-47))
    else:
        print(descendants)


def request(url):
    custom_headers = {
        'user-agent' : USER_AGENT,
        'accept': "text/html;charset=UTF-8"
    }
    response = requests.get(url, headers=custom_headers)
    response.encoding = "utf-8"
    return response.text

def encontrarTitulo(tag):
    return tag.has_attr('width') and tag['width'] == "201" and " " in tag.string

def matchSchedule(descNumber):
    return descNumber == 83 or descNumber == 83 + EXTRA_SCHEDULE or descNumber == 83 + 2*EXTRA_SCHEDULE or descNumber == 83 + 3* EXTRA_SCHEDULE or descNumber == 83 + 4*EXTRA_SCHEDULE

scrape()