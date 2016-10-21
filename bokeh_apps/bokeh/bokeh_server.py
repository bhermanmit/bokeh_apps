"""Provides the Bokeh server.
"""

import bokeh.command.util
import bokeh.server.server
import bokeh_apps.bokeh
import click
import json
import multiprocessing
import os
import setproctitle
import socket


class BokehServer(object):

    """Starts/Stops Bokeh Server.
    """

    def __init__(self, bokeh_port=None, http_port=None):

        self._host = 'localhost'
        self._http_port = http_port

        # get IP and port
        if bokeh_port is None:
            bokeh_socket = socket.socket()
            bokeh_socket.bind((host, 0))
            self._ip_addr, self._bokeh_port = bokeh_socket.getsockname()
        else:
            self._bokeh_port = int(bokeh_port)
            self._ip_addr = socket.gethostbyname(self._host)

        # get HTTP port
        if self._http_port is None:
            self._http_port = int(os.environ["BOKEH_HTTP_PORT"])
        else:
            self._http_port = int(self._http_port)

        self._started = False
        self._server = None
        self._proc = None

        options_dir = os.path.join(os.path.expanduser('~'), '.bokeh')
        if not os.path.exists(options_dir):
            os.mkdir(options_dir)

        bokeh_options = {
            'host': self._host,
            'http-port': self._http_port,
            'bokeh_port': self._bokeh_port,
        }

        with open(os.path.join(options_dir, '.bokeh-web-ui.json'), 'w') as handle:
            json.dump(bokeh_options, handle, indent=2)

        os.environ['BOKEH_PORT'] = str(self._http_port)

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
    def bokeh_port(self):

        """The port where the Bokeh server is listening.

        Type
        ----
        int
        """

        return self._bokeh_port

    @property
    def http_port(self):

        """The HTTP port where Bokeh fetches data.

        Type
        ----
        int
        """

        return self._http_port

    def start(self):

        """Starts the Bokeh server.
        """

        dirname = os.path.dirname(__file__)
        applications_path = [os.path.join(dirname, app) for app in
                             bokeh_apps.bokeh.APPLICATIONS]
        applications = bokeh.command.util.build_single_handler_applications(
            applications_path, {})

        server_kwargs = {
            'port': self._bokeh_port,
            'address': self._ip_addr,
            'host': ['{}:{}'.format(self._ip_addr, self._bokeh_port)],
            'check_unused_sessions_milliseconds': 50,
            'unused_session_lifettime_milliseconds': 1,
        }

        self._server = bokeh.server.server.Server(
            applications, **server_kwargs)

        self._proc = multiprocessing.Process(target=self._start_process)
        self._proc.start()

        print('Bokeh server started at http://{}:{}'.format(self._ip_addr,
                                                            self._bokeh_port))

    def _start_process(self):

        """Starts Bokeh server on forked process.
        """

        setproctitle.setproctitle('bokeh-server')
        self._server.start()

    def stop(self):

        """Stops the Bokeh server.
        """

        if self._started:

            self._proc.terminate()
            self._proc.join()
            self._proc = None
            self._started = False

    def __del__(self):
        self.stop()


@click.command()
@click.option('--bokeh-port', type=int)
@click.option('--http-port', default=None, type=int)
def main(bokeh_port, http_port):
    bokeh_server = BokehServer(bokeh_port, http_port)
    bokeh_server.start()
