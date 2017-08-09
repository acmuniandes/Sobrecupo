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
LOG_CLASS_SEPARATOR = '---------------------------------------------'
LOG_DEPT_SEPARATOR = '============================================================='
LOG_FREQUENCY = 2400
SEMESTRAL_END = "25/11/17"
DB_POSTING = "https://tu-salon-redis.herokuapp.com/devMode/post/classroomInfo"

#Global variables--------------

classList = []
errorCounter = 0
processString = ""
#Pointer used inside the loop to recall information between <table> tags
classPointer = None   

#Classes-----------------------

#Models neccesary information for a single class' schedule (a class may have multiple schedules)
#Contains weekdays, time (hhmm - hhmm), classroom and start/end dates
class Schedule:
    #Attributes set in 'constructor' method
    def __init__(self, weekdays, classTime, classroom, dateStart, dateEnd):
        self.weekdays = weekdays
        self.classTime = classTime
        self.classroom = classroom
        self.dateStart = dateStart
        self.dateEnd = dateEnd

    def toString(self):
        return self.classroom + "<<" + self.classTime + "<<" + self.weekdays + "<<" + self.dateStart + "<<" + self.dateEnd

#Models a course-class. Contains it's name, schedules and teacher's name.
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

#Models a classroom, contains its base schedule and a list of exceptions
class Classroom:
    #'constructor' method:
    def __init__(self, _id):
        self._id = _id
        #Initialize an empty matrix[x][y], with x being weekdays [0-5] (Monday to Saturday) and y schedules
        #This matrix models base (semestral) classroom behaviour
        self.baseSchedules = [['' for x in range(0)] for x in range(6)]
        #Attribute which models base schedule exceptions
        self.exceptions = []

    def post(self, schedule):
        print("posting: " + self._id + " " + str(schedule) + " // " + debugSchedule(schedule))
        if schedule.dateEnd == SEMESTRAL_END:

            #Parses weekdays string to weekday number (returns a list)
            numDays = weekdaysToNumber(schedule.weekdays)

            #Appends to corresponding matrix day
            for day in numDays:
                self.baseSchedules[day].append(schedule)
        else:
            self.exceptions.append(schedule)
        
        print("---endPosting---")
        counter = 0
        for day in self.baseSchedules:
            print("   d[" + str(counter) + "]: " + str(len(day)))
            counter += 1

    def toDictionary(self):
        dictionary = {}
        dictionary['_id'] = self._id

        dayCounter = 0
        for day in self.baseSchedules:
            schList = []
            for schedule in day:
                schList.append(schedule.toString)
            dictionary[str(dayCounter)]= str(schList)
            dayCounter += 1

        return dictionary


#Models an schedule exception: not-semestral classroom assignment
class _Exception:
    #'constructor' method:
    def __init__(self, time, dateStart, dateEnd, weekday):
        self.time = time
        self.dateStart = dateStart
        self.dateEnd = dateEnd
        self.weekday = weekday
        
#Methods-----------------------

#From local index file, extracts and scrapes links
def scrape():

    mainPage = None
    with open('indexReg.html', 'r') as file:
        mainPage = file.read()

    depSoup = BeautifulSoup(mainPage, 'html5lib')

    for link in depSoup.find_all('a', href=True):
        scrapeDep(link)

#Given an <a> tag with a department href, requests the url and scrapes Tables
def scrapeDep(depTag):

    global firstTable
    global isTitleTable
    global processString

    #Stores the url from the tag, slicing used to remove URL first part
    depHTML = depTag['href'][37:-1]

    #Logging events
    print("Entering: " + depHTML)
    processString += "\n" + LOG_DEPT_SEPARATOR + "\n" + depTag['href'][83:-1] + "\n" + LOG_DEPT_SEPARATOR

    if isRelative(depHTML):
        depHTML = BASE_URL + depHTML

    depPage = request(depHTML)
    
    depSoup = BeautifulSoup(depPage, 'html5lib')
    #Set firstTable to true: entering to a new dep
    firstTable = True
    isTitleTable = True

    for tableTag in depSoup.find_all(findValidTables):
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
    global classList

    #Determine how many descendants the actual <table> tag has
    descendants = len(list(tableTag.descendants))
    #print("desc: " + str(descendants))

    #Check if it is a schedules section
    schedules = 0
    isTitleTable = tableTag['width'] == '575'

    #If so, check how many schedules the class has
    if not isTitleTable:
        schedules = matchSchedule(descendants)

    if firstTable:
        print("HeadTable: " + str(descendants))
        firstTable = False
    elif schedules or not isTitleTable:
        
        #Adds schedules and teacher's name to a new _Class object (global classPointer)
        iterateSchedules(tableTag, schedules)
        #print (tableTag.find('font', class_ ='texto4').string.strip() + ' desc = ' + str(descendants))

        if validateClass(classPointer):
            classList.append(classPointer)
            logProcess(classPointer)
            print("----" + classPointer.name + " added----" + classPointer.teacher)
        else:
            print("----" + classPointer.name + " dismissed----" + " teacher: " + str(classPointer.teacher))
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
    else: #Unreachable code since boolean iteration implementation
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

        if schNum < 5:
            #Extracts it's info into an Schedule object and adds it to the list
            scheduleList.append(extractSchedule(actualTag))
        else:
            scheduleList.append(generalSchExtraction(actualTag))

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

def generalSchExtraction(tag):
    info = tag.find_all('td')
    weekdays = info[1].string.strip()
    classTime = info[2].string.strip()
    classroom = info[3].string.strip()
    dateStart = info[4].string.strip()
    dateEnd = info[5].string.strip()

    return Schedule(weekdays, classTime, classroom, dateStart, dateEnd)

#TODO finish serializing methods
#Using the given info from scraping, re-organizes it to simplify DB posting. Also generates per-classroom files
def serializeClasses(classList):
    classrooms = []
    for clss in classList:
        for schedule in clss.schedules:
            if not classroomInList(classrooms, schedule.classroom):
                addClassroom(classrooms, schedule)
            postClassroomInfo(classrooms, schedule)
    
    logClassrooms(classrooms)

    print("After log: ----")
    for classroom in classrooms:
        print("  " + classroom._id)
    return classrooms

def postDB(base, exceptions):
    
    #Post base schedules & exceptions

    for classroom in base:
        #Generate JSON for DB posting, includes base schedules and exceptions
        info = classroom.toDictionary()
        info['password'] = os.environ.get('REDIS_URL')
        requests.post(DB_POSTING, info)


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

def logProcess(clss):
    global processString
    string = "\n" + LOG_CLASS_SEPARATOR + "\n" + clss.name + " {" + clss.teacher + "}"
    for schedule in clss.schedules:
        string += "\n   " + debugSchedule(schedule)
    processString += string
    if len(processString) > LOG_FREQUENCY:
        log(processString)
        processString = ""

#Writes in log.log file the desired string
#In order to write a new line add the line skip to the beginning of the string
def log(strng):
    with open('Log.log', 'a') as file:
        file.write(strng)

#Checks wether a classrooms is within the given list
def classroomInList(classrooms, classroom):
    for sClassroom in classrooms:
        if classroom == sClassroom._id:
            return True
    return False

#Creates a Classroom object using schedule parámeter and appends it to the classes list
def addClassroom(classrooms, schedule):
    classroom = Classroom(schedule.classroom)
    classrooms.append(classroom)

#completes _Class object in classes list from schedeule parameter
#The class exists in the classList
def postClassroomInfo(classrooms, schedule):
    pointer = None
    for classroom in classrooms:
        if classroom._id == schedule.classroom:
            pointer = classroom
            break
    
    pointer.post(schedule)

def weekdaysToNumber(weekdays):
    numbers = []
    print("wkd param: " + str(weekdays))
    if "L" in weekdays:
        numbers.append(0)
    if "M" in weekdays:
        numbers.append(1)
    if "I" in weekdays:
        numbers.append(2)
    if "J" in weekdays:
        numbers.append(3)
    if "V" in weekdays:
        numbers.append(4)
    if "S" in weekdays:
        numbers.append(5)

    if len(numbers) < 1:
        print("Warning! invalid weekdays: " + weekdays)

    return numbers   

#For each classroom creates a file with its information. Also creates a final JSON with all the info
def logClassrooms(classrooms):
    for classroom in classrooms:
        with open('classroomsBase/' + classroom._id + ".classroom", 'w') as file:
            #Write info
            dayCounter = 0
            for day in classroom.baseSchedules:
                file.write("\n" + LOG_CLASS_SEPARATOR + "Day: " + str(dayCounter) + " // Sch's: " + str(len(day)) + " " + LOG_CLASS_SEPARATOR)
                for schedule in day:
                    file.write("\n" + debugSchedule(schedule))
                dayCounter += 1


def generateExceptionsDictionary(exceptions):

    for exception in exceptions:


#Tag recognition Methods(bs4)--

#Accepts tags that aren't marked
def detectScheduleTR(tag):
    return tag.name == "tr" and tag.get(MARKER) is None


def findTitle(tag):
    return tag.has_attr('width') and tag['width'] == "156" and " " in tag.string

def findValidTables(tag):
    desc = len(list(tag.descendants))
    return tag.name == 'table' and tag['cellspacing'] == '1'and desc != 25 and desc != 11

#Excecution
scrape()
info = serializeClasses(classList)
postDB(info)
