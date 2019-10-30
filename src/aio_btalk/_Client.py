
from asyncio import open_connection, Future, get_event_loop, create_task, Queue
from logging import getLogger
from yaml import load, dump
try:
    from yaml import CLoader as Loader, CDumper as Dumper
except ImportError:
    from yaml import Loader, Dumper

class Client(object):
    def __init__(self, reader, writer, loop=None):
        self.__log = getLogger('Client')
        self._reader = reader
        self._writer = writer
        self._host = None
        self._port = None
        self._loop = loop or get_event_loop()
        self._queue = Queue()
        self._processing = self._loop.create_task(self._read_responses())
        print(self._processing)

    @classmethod
    async def connect(cls, host, port, loop=None):
        reader, writer = await open_connection(host, port, loop=loop)
        cli = Client(reader, writer, loop=loop)
        cli._host = host
        cli._port = port
        return cli

    async def _read_responses(self):
        """ Read operation responses
        """
        self.__log.debug("Read server response")
        while True:
            req = await self._queue.get()
            status_line = await self._reader.readuntil(separator=b'\r\n')
            self.__log.debug('status_line = {status_line!r}'.format(status_line=status_line))
            if b' ' in status_line:
                status_code, size = status_line.split(b' ', 1)
                size = int(size)
                print(status_code, size)
                body = await self._reader.read(size)
                print(body)
                await self._reader.readuntil(separator=b'\r\n')
                req.set_result(body)
            else:
                req.set_result(status_line)
            #
            print("--- Packet complete ---")

    #  It's not a coroutine, it must return future to allow pipelining
    async def send_command(self, *args, body=None):
        self.__log.debug("Sending {args!r} ({body!r})".format(args=args, body=body))
        chunks = []
        for arg in args:
            arg = str(arg)
            if any([' ' in arg, '\r' in arg, '\n' in arg]):
                raise ArgumentError('Invalid char in argument')
            chunks.append(arg.encode('ascii'))
        if body is not None:
            if isinstance(body, str):
                body = body.encode('utf-8')
            if isinstance(body, bytes):
                raise ArgumentError('Invalid body type')
            chunks.append(str(len(body)).encode('ascii'))
        req = b' '.join(chunks) + b'\r\n'
        if body is not None:
            req += body + b'\r\n'
        fut = Future(loop=self._loop)
        self._writer.write(req)
        await self._writer.drain()
        await self._queue.put(fut)
        return fut

    async def stats(self):
        """ The stats command gives statistical information about the system as a whole.
        """
        self.__log.debug('C> stats')
        resp = await self.send_command('stats')
        body = await resp
        self.__log.debug('S> {body!r}'.format(body=body))
        result = load(body, Loader=Loader)
        return result
