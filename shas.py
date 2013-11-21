# -*- coding: utf-8 -*-
"""Simple Home Automation Service server.


"""
from __future__ import unicode_literals

from flask import (
    json, render_template, Flask)
from flask_sockets import Sockets

app = Flask(__name__)
sockets = Sockets(app)

@sockets.route('/bus')
def bus(ws):
    while True:
        message = ws.receive()
        if not message:
            continue
        data = json.loads(message)
        data['text'] += '-XXX'
        message = json.dumps(data)
        ws.send(message)


@app.route('/')
def home():
    return render_template('index.html')


if __name__ == '__main__':
    #app.run(debug=True)
    from gevent import pywsgi
    from geventwebsocket.handler import WebSocketHandler
    app.debug = True
    server = pywsgi.WSGIServer(
        ('', 8000), app, handler_class=WebSocketHandler)
    server.serve_forever()
