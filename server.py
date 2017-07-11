import os
import redis
import logging
import datetime

from flask import Flask , send_from_directory, render_template, url_for, request

r = redis.from_url(os.environ.get("REDIS_URL"))

app = Flask(__name__)

#"Landing page"
@app.route('/')
def webprint():
    return render_template('index.html')

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

#DevMode Handling------------------------------------

#Returns devMode.html [GET] #Checks login credentials [POST]
@app.route('/devMode', methods = ['POST', 'GET'])
def devMode():

    if request.method == 'GET':
        r.incr('devModeGet')
        return render_template('devMode.html')
    elif request.method == 'POST':
        pss = request.get_json() or request.form
        if checkPassword(pss['password'], request.environ['REMOTE_ADDR']):
            return os.environ.get('PASSWORD_MESSAGE')
        else:
            return 'quePasoAmiguitoxdxd'
    else:
        return '¿?'

#Recalls the failed log attemps of devMode
@app.route('/devMode/recall/logAttempts', methods = ['POST'])
def recallDB():
    pss = request.get_json() or request.form
    if checkPassword(pss['password'], request.environ['REMOTE_ADDR']):
        try:
            return str(r.lrange('devModeGetList', 0, -1))
        except Exception as error:
            return formatError(error)
    else:
        return 'la pulenta oe'

#Checks for password and logs failed attempts 
def checkPassword(password, ip):
    date = str(datetime.datetime.utcnow())
    attempt = password == os.environ.get('REDIS_URL')
    if not attempt:
        r.lpush('devModeGetList', "*IP: " + ip + " // " + "Timestamp: " + date + " // Attempt: " + password + "\n")
    return attempt

#Format function to redis errors
def formatError(error):
    msg = 'Type: ' + type(error) + '\n'
    msg += 'Exception: ' + error
    return msg