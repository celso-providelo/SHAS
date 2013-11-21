# -*- coding: utf-8 -*-
"""Simple Home Automation Service server.


"""
from __future__ import unicode_literals
import datetime

from flask import (
    json, render_template, Flask)
from flask_sockets import Sockets
from gevent import spawn, spawn_later


app = Flask(__name__)
sockets = Sockets(app)
app.debug = True


def send_event(ws, status):
    data = {
        'label': 'Movimento Sala TV',
        'action': status,
        'timestamp': datetime.datetime.now().isoformat(),
    }
    message = json.dumps(data)
    ws.send(message)

    if status == 'ON':
        status = 'OFF'
    else:
        status = 'ON'

    spawn_later(20, send_event, ws, status)


@sockets.route('/bus')
def bus(ws):
    while True:
        message = ws.receive()
        if not message:
            continue

        data = json.loads(message)
        if data.get('action') == 'start':
            spawn(send_event, ws, 'ON')
            continue

        data['timestamp'] = datetime.datetime.now().isoformat()
        message = json.dumps(data)
        ws.send(message)


@app.route('/')
def home():
    return render_template('index.html')


if __name__ == '__main__':
    #app.run(debug=True)
    from gevent import pywsgi
    from geventwebsocket.handler import WebSocketHandler
    server = pywsgi.WSGIServer(
        ('', 8000), app, handler_class=WebSocketHandler)
    server.serve_forever()
