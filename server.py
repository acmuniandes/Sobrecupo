import os
import redis
import logging
import datetime
import json

from flask import Flask , send_from_directory, render_template, url_for, request, jsonify

#Redis instance from heroku
r = redis.from_url(os.environ.get("REDIS_URL"), db =None, decode_responses = True)

app = Flask(__name__)

FAIL_MESSAGE = 'la pulenta oe'

data = None
with open('classrooms.json') as json_data:
    data = json.load(json_data)


#"Landing page"
@app.route('/')
def webprint():
    global data
    return render_template('index.html')

#Returning JSON
@app.route('/salones')
def salones():
    global data
    return json.dumps(data, ensure_ascii=False)

#Returning invalid-posted classrooms
@app.route('/salones/invalidos')
def salonesInvalidos( methods = ['POST', 'GET']):
    if request.method == 'GET':
        return r.smembers("invalidos")

    elif request.method == 'POST':
        info = request.get_json() or request.form #Matching Axios request type
        print("Adding invalid classroom: " + info['classroom'])
        r.sadd("invalidos", info['classroom'])
        return "¡Se registró exitosamente el salón!"
    else:
        #By default, before entering the function, if the method does not match, an unsupported
        #Server method error will be returned
        return FAIL_MESSAGE


#Saves the string <strng> in the DB
@app.route('/db/<strng>')
def saveInDB(strng):
    r.lpush('db', '%s' % strng)
    return 'OK'

#Recalls the stored info in the DB
@app.route('/db/recall/test', methods = ['GET'])
def recallDB():
    try:
        return str(r.lrange('db', 0, -1))
    except Exception as error:
        return formatError(error)

#DevMode Handling---------------------------------------------

#Returns devMode.html [GET] #Checks login credentials [POST]
@app.route('/devMode', methods = ['POST', 'GET'])
def devMode():
    if request.method == 'GET':
        r.incr('devModeGet')
        return render_template('devMode.html')
    elif request.method == 'POST':
        pss = request.get_json() or request.form #Matching Axios request type
        if checkPassword(pss['password'], pss['info']):
            return os.environ.get('PASSWORD_MESSAGE')
        else:
            return FAIL_MESSAGE
    else: #Message for other methods (DELETE, PUT, CONNECT, ...)
        return '¿?'

#Recalls the failed log attemps of devMode
@app.route('/devMode/recall/logAttempts', methods = ['POST'])
def recallLogAttempts():
    pss = request.get_json() or request.form
    if checkPassword(pss['password'], pss['info']):
        try:
            return str(r.lrange('devModeGetList', 0, -1))[1:-2]
        except Exception as error:
            return formatError(error)
    else:
        return FAIL_MESSAGE

#Recalls the times devMode's URL was accessed
@app.route('/devMode/recall/getTimes', methods = ['POST'])
def recallGetTimes():
    pss = request.get_json() or request.form
    if checkPassword(pss['password'], pss['info']):
        try:
            return str(r.get('devModeGet'))
        except Exception as error:
            return formatError(error)
    else:
        return FAIL_MESSAGE

#Posts classroom information
@app.route('/devMode/post/classroomInfo', methods = ['POST'])
def postClassroomInfo():
    pss = request.get_json() or request.form
    if checkPassword(pss['password'], pss['info']):
        r.append("classrooms", "<<" + str(pss))
        return "yay!"
    else:
        return "Wrong password"

@app.route('/devMode/get/classroomInfo', methods = ['POST'])
def getClassroomInfo():
    pss = request.get_json() or request.form
    if checkPassword(pss['password'], pss['info']):
        return r.get("classrooms")
    else:
        return "Wrong password"

#Non-server functions-----------------

#Checks for password and logs failed attempts 
def checkPassword(password, info):
    date = str(datetime.datetime.utcnow())
    attempt = password == os.environ.get('REDIS_URL')
    if not attempt:
        r.lpush('devModeGetList', "Info: " + info + " --- " + "Timestamp: " + date + " // Attempt: " + password + "\n")
    return attempt

#Format function to redis errors
def formatError(error):
    msg = 'Type: ' + type(error) + '\n'
    msg += 'Exception: ' + error
    return msg