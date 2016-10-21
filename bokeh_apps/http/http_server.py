"""Provides the HTTPServer class.
"""

import click
import json
import multiprocessing
import setproctitle
import socket
import tornado.ioloop
import tornado.httpserver
import tornado.web

HTTP_DATA = {
    'memory': {},
}


class MemoryHandler(tornado.web.RequestHandler):

    """HTTP handler for memory.
    """

    def get(self):

        """Respond to HTTP GET.
        """

        self.write(HTTP_DATA['memory'])

    def post(self):

        """Respond to HTTP POST.
        """

        data = json.loads(self.request.body)
        for key, val in data.iteritems():
            HTTP_DATA['memory'][key] = val


class HTTPServer(object):

    """Starts/Stops HTTP Server.
    """

    def __init__(self, http_port=None):

        self._host = 'localhost'

        # get IP and port
        if http_port is None:
            http_socket = socket.socket()
            http_socket.bin((self._host, 0))
            self._ip_addr, self._http_port = http_socket.getsockname()
        else:
            self._http_port = int(http_port)
            self._ip_addr = socket.gethostbyname(self._host)

        self._started = False
        self._server = None
        self._proc = None

    @property
    def host(self):

        """Name or IP of host.

        Type
        ----
        str
        """

        return self._host

    @property
    def ip_addr(self):

        """IP address where Bokeh server exists.

        Type
        ----
        str
        """

        return self._ip_addr

    @property
    def http_port(self):

        """The HTTP port where Bokeh fetches data.

        Type
        ----
        int
        """

        return self._http_port

    def start(self):

        """Starts HTTP server.
        """

        application = tornado.web.Application([
            (r'/memory.json', MemoryHandler)
        ])

        self._server = tornado.httpserver.HTTPServer(
            application, io_loop=tornado.ioloop.IOLoop.current())

        self._proc = multiprocessing.Process(target=self._start_process)
        self._proc.start()

        self._started = True

    def stop(self):

        """Stops HTTP server.
        """

        if self._started:

            self._server.unlisten()
            self._server.stop()
            self._server.io_loop.close()
            self._proc.terminate()
            self._proc.join()

            self._started = False
            self._server = None
            self._proc = None

    def _start_process(self):

        """Starts HTTP server on forked process.
        """

        setproctitle.setproctitle('http-server')
        self._server.listen(self._http_port)
        tornado.ioloop.IOLoop.current().start()

    def __del__(self):
        self.stop()


@click.command()
@click.option('--http-port', type=int, default=None)
def main(http_port):
    http_server = HTTPServer(http_port)
    http_server.start()
