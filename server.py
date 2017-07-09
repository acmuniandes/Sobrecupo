import os
import redis
import logging
from flask import Flask , send_from_directory, render_template, url_for

r = redis.from_url(os.environ.get("REDIS_URL"))

app = Flask(__name__)

#"Landing page"
@app.route('/')
def webprint():
    return render_template('index.html')

#Returns .js file (Vue)
@app.route('/app.js')
def Vue():
    return send_from_directory(filename = 'app.js', directory = 'scripts')

#Saves the string <strng> in the DB
@app.route('/db/<strng>')
def saveInDB(strng):
    r.lpush('db', '%s' % strng)
    return 'OK'

#Recalls the stored info of the DB
@app.route('/db/recall')
def recallDB():
    try:
        return str(r.lrange('db', 0, -1))
    except Exception as error:
        msg = ''
        msg += 'Type : ' + type(error) + '\n'
        msg += 'Exception: ' + error
        return msg
    
