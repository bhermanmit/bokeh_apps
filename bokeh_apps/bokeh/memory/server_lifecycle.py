"""Gathers data to update plot.
"""
from __future__ import print_function

import bokeh_apps.bokeh
import json
import os
import tornado.gen
import tornado.httpclient


CLIENT = tornado.httpclient.AsyncHTTPClient()

MESSAGES = bokeh_apps.bokeh.MESSAGES

OPTIONS_PATH = os.path.join(
    os.path.expanduser('~'), '.bokeh', '.bokeh-web-ui.json')

if os.path.exists(OPTIONS_PATH):
    with open(OPTIONS_PATH, 'r') as handle:
        OPTIONS = json.load(handle)
else:
    raise IOError("Can't locate Bokeh server from " + OPTIONS_PATH)


@tornado.gen.coroutine
def memory():

    """Gets memory from HTTP server.
    """

    try:
        response = yield CLIENT.fetch(
            'http://{host}:{http-port}/memory.json'.format(**OPTIONS))
    except tornado.httpclient.HTTPError:
        print('memory.json HTTP route failed.')
    msg = json.loads(response.body.decode())
    if msg:
        for key, val in msg.iteritems():
            MESSAGES['memory'][key] = val


def on_server_loaded(server_context):

    """Called when server is loaded.
    """

    server_context.add_periodic_callback(memory, 500)
