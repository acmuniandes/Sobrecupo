import os
import requests
from bs4 import BeautifulSoup

#Constants---------------------

BASE_URL = "https://registroapps.uniandes.edu.co"
USER_AGENT = 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/535.19 (KHTML, like Gecko) Chrome/18.0.1003.1 Safari/535.19 Awesomium/1.7.4.2'
ACCEPT_LANGUAGE = "es-ES,es;q=0.8,en-US;q=0.5,en;q=0.3"
EXTRA_SCHEDULE = 26
MARKER = 'marked'
MARKED = 'True'
LOG_SEPARATOR = '---------------------------------------------'
LOG_FREQUENCY = 2400

#Global variables--------------

classList = []
errorCounter = 0
#Pointer used inside the loop to recall information between <table> tags
classPointer = None   

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

#Models a university course-class. Contains it's name, schedules and teacher's name.
class _Class:
    #Attributes set in 'constructor' method
    def __init__(self, name):
        self.name = name
        self.teacher = None
        self.schedules = None
        #Debugging
        #print(name)
    
    def completeInfo(self, schedules, teacher):
        self.teacher = teacher
        self.schedules = schedules
        #Debugging
        #for schedule in schedules:
        #    print("  " + debugSchedule(schedule))

#Methods-----------------------

def scrape():

    mainPage = None
    with open('indexReg.html', 'r') as file:
        mainPage = file.read()

    depSoup = BeautifulSoup(mainPage, 'html5lib')

    for link in depSoup.find_all('a', href=True):
        scrapeDep(link)

def scrapeDep(depTag):

    global firstTable
    global isTitleTable

    #Stores the url from the tag
    depHTML = depTag['href'][37:-1]

    print("Entering: " + depHTML)

    if isRelative(depHTML):
        depHTML = BASE_URL + depHTML

    depPage = request(depHTML)
    
    depSoup = BeautifulSoup(depPage, 'html5lib')
    #Set firstTable to true: entering to a new dep
    firstTable = True
    isTitleTable = True

    for tableTag in depSoup.find_all('table', cellspacing="1"):
        extractTables(tableTag)

#Global variables used for iteration
firstTable = True
#Boolean iterator for table scraping
isTitleTable = True

def extractTables(tableTag):

    global classPointer
    global firstTable
    global isTitleTable
    global errorCounter
    global processString

    #Determine how many descendants the actual <table> tag has
    descendants = len(list(tableTag.descendants))

    #Check if it is a schedules section
    schedules = 0
    isTitleTable = tableTag['width'] == '575'

    if not isTitleTable:
        schedules = matchSchedule(descendants)

    if firstTable:
        print("HeadTable: " + str(descendants))
        firstTable = False
    elif schedules or not isTitleTable:
        #TODO Fix for dep: automatizaci-on de procesos
        
        #Adds schedules and teacher's name to currentClass pointer
        iterateSchedules(tableTag, schedules)
        #print (tableTag.find('font', class_ ='texto4').string.strip() + ' desc = ' + str(descendants))

        if validateClass(classPointer):
            classList.append(classPointer)
            logProcess(classPointer)
            print("----" + classPointer.name + " added----" + classPointer.teacher)
        else:
            print("----" + classPointer.name + " dismissed----  sch: " + str(classPointer.schedules) + " teacher: " + str(classPointer.teacher) + " sch': " + str(schedules))
        #Reset classPointer
        classPointer = None       
        isTitleTable = True 
        
    elif descendants >= 77 and descendants < 370 and isTitleTable:
        #TODO Prettify/document next 8 lines
        try:
            classPointer = _Class(tableTag.find_all(findTitle)[0].string.strip())
            isTitleTable = False
        except Exception as error:
            print(str(error) + " desc = " + str(descendants) + " - 47 = " + str(descendants-47) + " boolean: " + str(isTitleTable) + " counter = " + str(errorCounter) + " \n\n" + str(tableTag))
            log(processString)
    else:
        print(descendants)





#Function to tell if a <table> tag matches a schedule section based on it's number of descendants
#If it's a schedule section returns how many schedules are there, if not, returns 0
def matchSchedule(numOfDescendants):
    fitsSchedule = False
    schedules = 0
    #TODO Check if there are courses with more than 9 different schedules
    for c in range(10):
        schRange = 83 + c*EXTRA_SCHEDULE
        fitsSchedule = numOfDescendants == schRange or numOfDescendants == schRange+1
        if fitsSchedule:
            schedules = c + 1
            break
    return schedules

#Function to extract schedule information from <table> tag for the current class
# <table> tag may contain multiple schedules. The function returns a list with initialized schedules
def iterateSchedules(parentTag, schedules):
    #Mark first <tr>
    actualTag = parentTag.find('tr')[MARKER] = MARKED


    #Find <tr> tags with schedule info, the last one contains teacher's name
    scheduleTRs = parentTag.find_all(detectScheduleTR)
    #print("TR list len = " + str(len(scheduleTRs)) + "// Schedules var = " + str(schedules))
    #Initializate object's return list
    scheduleList = []

    #Used fixed range b/c last one is not a schedule
    for schNum in range(schedules):
        #Picks a <tr> tag containing a schedule
        actualTag = scheduleTRs[schNum]
        #Extracts it's info into an Schedule object and adds it to the list
        scheduleList.append(extractSchedule(actualTag))

    #Extracts current class' teacher(s) name
    actualTag = scheduleTRs[schedules]
    teacher = actualTag.find('td', width='172').string.strip()

    #Multiple teacher detection
    #extra = actualTag.find_all('td')
    #print (str(len(extra)))

    #Finally, add info to current class pointer
    classPointer.completeInfo(scheduleList, teacher)

#Returns a Schedule object based on a <tr> tag
def extractSchedule(tag):
    info = tag.find_all('td', width='171')
    #Explicit info values
    weekdays = tag.find('td', width='172').string.strip()
    classTime = info[0].string.strip()
    classroom = info[1].string.strip()
    dateStart = info[2].string.strip()
    dateEnd = info[3].string.strip()

    #Instantiates Schedule object with the given info
    return Schedule(weekdays, classTime, classroom, dateStart, dateEnd)

#Auxiliary methods-------------

def isRelative(url):
    return url.startswith('/')

def request(url):

    s = requests.Session()

    custom_headers = {
        'User-Agent' : USER_AGENT,
        'Accept': "text/html;charset=UTF-8",
        'Accept-Language': ACCEPT_LANGUAGE,
        'Cookie': '__utma=154978747.1072089661.1499469016.1500390322.1500417611.7; __utmz=154978747.1500417611.7.2.utmcsr=google|utmccn=(organic)|utmcmd=organic|utmctr=(not%20provided); _ga=GA1.3.1072089661.1499469016; _gid=GA1.3.1963782703.1500382504; __utmb=154978747.5.10.1500417611; _gat=1; __utmc=154978747'
    }
    #response = requests.get(url, headers=custom_headers)

    jar = requests.cookies.RequestsCookieJar()
    jar.set('_utma', '154978747.1072089661.1499469016.1500386404.1500390322.6')
    jar.set('__utmz', "154978747.1023459016.1.1.utmctmccn=(direct)|utmcmd=(none)")
    jar.set('_ga', "GA1.3.1072089661.1499469016")
    jar.set('_gid', "GA1.3.1963782703.1500382504")
    jar.set('__utmc', "154978747")

    response = s.get(url, headers=custom_headers)
    response.encoding = "utf-8"
    return response.text

def debugSchedule(sch):
    debugStr = sch.classroom + " @" + sch.classTime + "[" + sch.weekdays + "]" + "(" + sch.dateStart + " to " + sch.dateEnd + ")"
    return debugStr

def validateClass(clss):
    valid = clss.name is not None and len(clss.name) > 3 and clss.schedules is not None and len(clss.schedules) >= 1
    if valid:
        valid = clss.schedules[0].classroom != "." or clss.schedules[0].classroom != ".NOREQ"
        valid = valid and len(clss.schedules[0].weekdays) >0
    return valid

processString = ""
def logProcess(clss):
    global processString
    string = "\n" + LOG_SEPARATOR + "\n" + clss.name + "{" + clss.teacher + "}"
    for schedule in clss.schedules:
        string += "\n   " + debugSchedule(schedule)
    processString += string
    if len(processString) > LOG_FREQUENCY:
        log(processString)
        processString = ""

def log(strng):
    with open('Log.log', 'a') as file:
        file.write(strng)
#Tag recognition Methods(bs4)--

#Accepts tags that aren't marked
def detectScheduleTR(tag):
    return tag.name == "tr" and tag.get(MARKER) is None


def findTitle(tag):
    return tag.has_attr('width') and tag['width'] == "156" and " " in tag.string

#Excecution
scrape()
