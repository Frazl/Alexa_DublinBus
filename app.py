from flask import Flask, render_template
from flask_ask import Ask, statement, question, session
import json
import requests 
import time 
import unidecode

app = Flask(__name__)
ask = Ask(app, "/")

def get_stop_information(stopNumber):
    request = requests.get("https://data.smartdublin.ie/cgi-bin/rtpi/realtimebusinformation?stopid="+str(stopNumber)+"&format=json")
    response = json.loads(request.content.decode('utf-8'))
    bus_count = len(response['results'])
    if bus_count == 1:
        s = "There is {:n} bus coming...".format(bus_count)
    elif bus_count < 1:
        s = "There are no busses scheduled to arrive at this stop..."
        return s
    else:
        s = "There are {:n} buses coming...".format(bus_count)
    for i in range(len(response['results'])):
        s += " There is a {:s} bus coming in {:s} minutes...".format(response['results'][i]['route'], response['results'][i]['duetime'])
    return s


@ask.launch 
def start_skill():
    welcome_message = 'What stop would you like information about?'
    return question(welcome_message)

@ask.intent("StopNumber", mapping={'Stop': 'Stop'})
def share_stop_number_informatoin(Stop):
    Stop = int(Stop)
    if 9 < Stop < 7712:
        print("see above")
        information = get_stop_information(Stop)
        return statement(information)
    else:
        return statement("{:n} is not a stop...".format(Stop))

@ask.intent("NegativeIntent")
def negative_intent():
    bye_text = "Rude for asking to me wake up then... I was having a nice nap... bye"
    return statement(bye_text)






if __name__ == '__main__':
    app.run(debug=True, port=5002)
