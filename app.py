from flask import Flask, render_template
from flask_ask import Ask, statement, question, session
import json
import requests
import time
import unidecode

app = Flask(__name__)
ask = Ask(app,"/headliner")

def get_headlines():
    user_pass_dict = {'user': 'USERNAME',
                      'passwd': 'PASSWORD',
                      'api_type': 'json'}
    sess = requests.Session()
    sess.headers.update({'User-Agent': 'Test for Alexa: Jay'})
    sess.post('https://www.reddit.com/api/login',data=user_pass_dict)
    time.sleep(1)
    url = 'https://reddit.com/r/tech/.json?limit=10'
    html = sess.get(url)
    data = json.loads(html.content.decode('utf-8'))
    titles = [unidecode.unidecode(listing['data']['title'])for listing in data['data']['children']]
    titles = '...'.join([i for i in titles])
    return titles

@app.route('/')
def homepage():
    return "Welcome to Headliner"

@ask.launch
def start_skill():
    welcome_message = 'Hello, Welcome to Techliner, would you like the news?'
    return question(welcome_message)

@ask.intent("YesIntent")
def share_headlines():
    headlines = get_headlines()
    headline_msg = 'Current world headlines are {}'.format(headlines)
    return statement(headline_msg)
@ask.intent("NoIntent")
def no_intent():
    quit = 'Okay, Thanks for calling Headliner,Bye'
    return statement(quit)


if  __name__ == '__main__':
    app.run(debug=True)





