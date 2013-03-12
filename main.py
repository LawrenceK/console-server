import logging
_log = logging.getLogger(__name__)

from twisted.internet import reactor

from consoleserver import console_server

if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG,
                        format='%(asctime)s %(levelname)s [%(funcName)s] %(message)s')
    console_server()
    _log.info("Starting twisted reactor")
    reactor.run()
