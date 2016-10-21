"""Worker A
"""
from __future__ import print_function

import click
import datetime
import json
import psutil
import random
import setproctitle
import sys
import time
import tornado.httpclient


@click.command()
@click.option('--ip-addr', default='localhost', type=str)
@click.option('--http-port', default=None, type=int)
@click.option('--hostname', default=None, type=str)
def main(ip_addr, http_port, hostname):

    """Main routine that posts data to HTTP server.
    """

    setproctitle.setproctitle('worker')

    start = datetime.datetime.now()

    data = {}

    data['host'] = hostname
    data['pid'] = psutil.Process().pid
    data['rank'] = 0

    client = tornado.httpclient.HTTPClient()

    while True:
        delta_time = datetime.datetime.now() - start
        delta_time = delta_time.seconds + delta_time.microseconds*10**-6
        data['time'] = delta_time
        data['memory'] = random.randint(0, 100)
        request = tornado.httpclient.HTTPRequest(
            'http://{}:{}/memory.json'.format(ip_addr, http_port),
            method='POST', body=json.dumps(data))
        client.fetch(request)
        time.sleep(1.0)

if __name__ == '__main__':
    sys.exit(main())
