#!/usr/bin/env python3

#import logging
#logging.basicConfig(level=logging.DEBUG)

from wsgiref.validate import validator
from spyne import Application, rpc, ServiceBase, Integer, Unicode, String
from spyne.protocol.soap import Soap11
from spyne.server.wsgi import WsgiApplication
from time import time_ns
from typing import List, Dict

cb = []
nicks : Dict[str, int]= {}

def reset_cb() -> None:
    global cb, nicks
    cb = []
    nicks = {}

def new_message(nick: str, message : str) -> int:
    '''Adds a new message to the chat buffer'''
    global nicks
    if nick not in nicks.keys():
        nicks[nick] = 0
    ts = time_ns()
    cb.append({"timestamp": ts, "nick": nick, "msg": message})
    return ts

def get_messages(nick: str) -> str:
    ts = 0
    if nick in nicks.keys():
        ts = nicks[nick]
    out : List[str] = []
    for c in cb:
        if c['timestamp'] > ts:
            out.append(c['nick'] + ': ' + c['msg'])
    nicks[nick] = time_ns()
    if len(out) > 0:
        return "\n".join(out)
    return ""

class ChatService(ServiceBase):
    @rpc(String, _returns=String)
    def getMsgs(ctx, nick):
        print(nick + ' is getting msgs')
        m = get_messages(nick)
        print(m)
        return m

    @rpc(String, String, _returns=Integer)
    def sendMsg(ctx, nick, msg):
        print(nick + " just sent " + msg);
        return new_message(nick, msg)
    
app = Application([ChatService], tns='example.chat.pdf', in_protocol=Soap11(), out_protocol=Soap11())

if __name__ == '__main__':
    from wsgiref.simple_server import make_server
    wsgi_app = WsgiApplication(app)
    server = make_server('0.0.0.0', 8000, wsgi_app)
    server.serve_forever()
