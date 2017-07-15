import os
import requests
from bs4 import BeautifulSoup

#Constants------------------

BASE_URL = "https://registroapps.uniandes.edu.co/"
USER_AGENT = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.95 Safari/537.36"
EXTRA_SCHEDULE = 26
MARKER = 'marked'
MARKED = 'True'

#Classes-----------------------

#Models neccesary information for a single class' schedule (a class may have multiple schedules)
#Contains weekdays, time (hhmm - hhmm), classroom and  start/end dates
class Schedule:
    #Attributes set in 'constructor' method
    def __init__(self, weekdays, classTime, classroom, dateStart, dateEnd):
        self.weekdays = weekdays
        self.classTime = classTime
        self.classroom = classroom
        self.dateStart = dateStart
        self.dateEnd = dateEnd

#
class _Class:
    #Attributes set in 'constructor' method
    def __init__(self, schedules, teacher):
        self.teacher = teacher
        self.name = None
        self.schedules = schedules

#Methods-----------------------

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

    #Pointer used inside the loop to recall information between <table> tags
    actualClass = None    

    for tableTag in depSoup.find_all('table', cellspacing="1"):
        extractTables(tableTag, actualClass)



def extractTables(tableTag, classPointer):
    #Determine how many descendants the actual <table> tag has
    descendants = len(list(tableTag.descendants))

    #Check if it is a schedules section
    schedules = matchSchedule(descendants)
    if schedules:
        #TODO Test current schedule scraping
        try:
            #Primitive class: contains schedules and teacher's name
            classPointer = iterateSchedules(tableTag, schedules)
            #print (tableTag.find('font', class_ ='texto4').string.strip() + ' desc = ' + str(descendants))
        except Exception as error:
            print (error)
    elif descendants >= 77 and descendants < 370:
        #TODO Finish _Class scraping and serializing
        try:
            print(tableTag.find_all(encontrarTitulo)[0].string.lstrip().rstrip())
        except Exception as error:
            print(str(error) + " desc = " + str(descendants) + " - 47 = " + str(descendants-47))
    else:
        print(descendants)





#Function to tell if a <table> tag matches a schedule section based on it's number of descendants
#If it's a schedule section returns how many schedules are there, if not, returns 0
def matchSchedule(numOfDescendants):
    fitsSchedule = False
    schedules = 0
    #TODO Check if there are courses with more than 8 different schedules
    for c in range(9):
        fitsSchedule = numOfDescendants == 83 + c*EXTRA_SCHEDULE
        if fitsSchedule:
            schedules = c + 1
            break
    return schedules

#Function to extract schedule information from <table> tag for the current class
# <table> tag may contain multiple schedules thus, the function returns a List
def iterateSchedules(parentTag, schedules):
    #Mark first <tr>
    actualTag = parentTag.find('tr')[MARKER] = MARKED

    #Find <tr> tags with schedule info, the last one contains teacher's name
    scheduleTRs = parentTag.find_all(detectScheduleTR)

    #Initializate object's return list
    scheduleList = []

    #Used fixed range b/c last one is not a schedule
    for schNum in range(schedules):
        #Picks a <tr> tag containing a schedule
        actualTag = scheduleTRs[schNum]
        #Extracts it's info into an Schedule object and adds it to the list
        scheduleList.append(extractSchedule(actualTag))

    #Finally, extract current class' teacher name
    actualTag = scheduleTRs[schedules]
    teacher = actualTag.find('td', width='172').string.strip()

    return _Class(scheduleList, teacher)

#Returns a Schedule object based on a <tr> tag
def extractSchedule(tag):
    info = tag.find_all('td', height='17')
    #Explicit info values
    weekdays = info[0].string.strip()
    classTime = info[1].string.strip()
    classroom = info[2].string.strip()
    dateStart = info[3].string.strip()
    dateEnd = info[4].string.strip()

    #Instantiates Schedule object with the given info
    return Schedule(weekdays, classTime, classroom, dateStart, dateEnd)

#Auxiliary methods-------------

def isRelative(url):
    return url.startswith('..')

def request(url):
    custom_headers = {
        'user-agent' : USER_AGENT,
        'accept': "text/html;charset=UTF-8"
    }
    response = requests.get(url, headers=custom_headers)
    response.encoding = "utf-8"
    return response.text

#Tag recognition Methods(bs4)--

#Accepts tags that aren't marked
def detectScheduleTR(tag):
    return tag.get(MARKER) == None


def encontrarTitulo(tag):
    return tag.has_attr('width') and tag['width'] == "201" and " " in tag.string

scrape()