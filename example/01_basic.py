#!/usr/bin/env -S python3 -B -u

from logging import getLogger, basicConfig, DEBUG, INFO
from aio_btalk import Client
from asyncio import get_event_loop, sleep

class Application(object):
    def __init__(self):
        self.__log = getLogger('Application')

    async def runProcessing(self):
        btc = await Client.connect(host='127.0.0.1', port=11300)
        #
        stats = await btc.stats()
        self.__log.debug('stats = {stats!r}'.format(stats=stats))
        #
        resp = await btc.send_command('reserve-with-timeout', 1)
        self.__log.debug('resp = {resp!r}'.format(resp=resp))
        status = await resp

    def run(self):
        self.__log.info('Start application.')
        loop = get_event_loop()
        loop.run_until_complete(self.runProcessing())
        loop.close()
        self.__log.info('Done.')


if __name__ == "__main__":
    basicConfig(level=DEBUG)
    app = Application()
    app.run()
