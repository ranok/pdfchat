#!/usr/bin/env python3

from flask import Flask
from zeep import Client
app = Flask(__name__)

c = Client("http://localhost:8000/?wsdl")

@app.route("/get_msgs/<nick>")
def get_msgs(nick):
    out = c.service.getMsgs(nick)
    if out is None:
        out = ""
    return out

@app.route("/send_msg/<nick>/<msg>")
def send_msg(nick, msg):
    return str(c.service.sendMsg(nick, msg))
