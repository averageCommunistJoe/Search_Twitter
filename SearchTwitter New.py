#import stuff
from temboo.Library.Twitter.Search import Tweets
from temboo.core.session import TembooSession

import MySQLdb
import json

from flask import Flask
from flask import request
import random

#name the app
app = Flask(__name__)

#defines neccessary variables
query = ''
queries = []
queriesstr = ''

#create the homepage
def updateHTML():
    global baseHTML
    global queriesstr
    baseHTML = '''
        <html>
          <head>
            <title>Home Page</title>
          </head>
          <body>
            <h1>Search Twitter!</h1>
                <form action="." method="POST">
                    <input type="text" name="QUERY">
                    <input type="submit" name="my-form" value="Send">
                </form>
            <h2>Previous Queries</h2>
                <form action="." method = "POST">
                    %s
                </form>
                <br>
            <h1>Results</h1>
                <br>
          </body>
        </html>
        ''' % \
        (queriesstr)
    print baseHTML
    print queriesstr

@app.route('/')
def index():
    updateHTML()
    return baseHTML

#The behind the scenes stuff
def Querying(query):
    tweets = []
    # Instantiate the Choreo, using a previously instantiated TembooSession object
    session = TembooSession('thepro', 'myFirstApp', '9199f88be73641709b1e7e10ba8b292b')
    tweetsChoreo = Tweets(session)

    # Get an InputSet object for the choreo
    tweetsInputs = tweetsChoreo.new_input_set()

    # Set inputs
    tweetsInputs.set_Count('100')
    tweetsInputs.set_AccessToken("1700018462-VIgKuyMKgkL8YM0kbPg3W64b0sJMg7f91Vfj5BP")
    tweetsInputs.set_Query(query)
    tweetsInputs.set_AccessTokenSecret("FZgDdIVFLedVo6zEmkjkBul5N4zxdudArmpjgZKF43OsV")
    tweetsInputs.set_ConsumerSecret("5YJ6xOpADS7GwRwbXGwwv1GYZa3SzvOv6l0Fcwx8Q")
    tweetsInputs.set_ConsumerKey("OjrSexpjVSHegwPEsHh2rA")

    # Execute choreo
    tweetsResults = tweetsChoreo.execute_with_results(tweetsInputs)

    data  = json.loads(tweetsResults.get_Response())

    #finds tweets and lists them
    for i in range(0,100):
        try:
            tweet = data["statuses"][i]['text']
            tweets.append(tweet)
        except IndexError:
            tweet = 'none'
    NHTML = ''
    for i in range(0,len(tweets)):
        NHTML += tweets[i] + '<br>'

    #Does the MySQL stuff (commented out because it slows it down)

##    db=MySQLdb.connect(host = 'localhost',user='root',passwd="swag",db="tweets")
##    cursor = db.cursor()
##    #cursor.execute("DROP TABLE IF EXISTS TWEETS")
##
##    sql = """CREATE TABLE IF NOT EXISTS TWEETS (
##             QUERY  CHAR(40) NOT NULL,
##             TWEET  BLOB
##             )"""
##
##    cursor.execute(sql)
##
##    #Inserts tweets into MySQLdb
##    for i in range(0,len(tweets)):
##        sql = "INSERT INTO TWEETS(QUERY, \
##               TWEET) \
##               VALUES ('%s', '%s')" % \
##               (query, tweets[i])
##
##        try:
##            cursor.execute(sql)
##            db.commit()
##        except:
##            db.rollback()

    return NHTML
    


##
##    #Finds the Tweets Related to the Query
##    sql = "SELECT * FROM TWEETS \
##           WHERE QUERY = '%s'" % (query)
##
##    try:
##        cursor.execute(sql)
##        results = cursor.fetchall()
##        for row in results:
##            question = row[0]
##            tweet = row[1]
##            print "query = %s, tweet = %s" % \
##                  (question, tweet)
##            
##    except:
##        print "Error: unable to fetch data"
##
##    #Saves Queries in table queries
##    #cursor.execute("DROP TABLE IF EXISTS QUERIES")
##    sql = """CREATE TABLE IF NOT EXISTS QUERIES (
##             QUERY  CHAR(40) NOT NULL
##             )"""
##    cursor.execute(sql)
##    for i in range(0,len(tweets)):
##        sql = "INSERT INTO QUERIES(QUERY, \
##               VALUES ('%s')" % \
##               (query)
##
##        try:
##            cursor.execute(sql)
##            db.commit()
##        except:
##            db.rollback()
##
##    print 'html is' + html

#take the form
@app.route('/', methods=['POST'])
def my_form_post():
    text = request.form['QUERY']
    print text
    addedHTML = Querying(text)
    global queriesstr
    queriesstr += '<a href = "http://127.0.0.1:5000/' + text + '">' + text + '</a>   '
    updateHTML()
    return baseHTML + addedHTML

@app.route('/<search>')
def show_search(search):
    addedHTML = Querying(search)
    return baseHTML + addedHTML


if __name__ == '__main__':
    app.run(host='0.0.0.0')
