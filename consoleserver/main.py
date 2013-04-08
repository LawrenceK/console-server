import logging
_log = logging.getLogger(__name__)

from twisted.internet import reactor


def main():
    logging.basicConfig(level=logging.DEBUG,
                        format='%(asctime)s %(levelname)s [%(funcName)s] %(message)s')
    import config
    config.set_config('/etc/consoleserver/config.ini')
    from consoleserver import console_server
    console_server()
    _log.info("Starting twisted reactor")
    reactor.run()

if __name__ == '__main__':
    main()
