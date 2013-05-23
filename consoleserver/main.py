import logging
_log = logging.getLogger(__name__)
import os
from twisted.internet import reactor

DEF_CONFIG_NAME = 'config.ini'
CONFIG_FILENAME = '/etc/consoleserver/config.ini'


def check_config_exists():
    if not os.path.exists(CONFIG_FILENAME):
        if not os.path.exists(os.path.dirname(CONFIG_FILENAME)):
            os.mkdir(os.path.dirname(CONFIG_FILENAME))
        import shutil
        shutil.copy2(os.path.join(os.path.dirname(os.path.abspath(__file__)), DEF_CONFIG_NAME), CONFIG_FILENAME)


def main():
    logging.basicConfig(level=logging.DEBUG,
                        format='%(asctime)s %(levelname)s [%(funcName)s] %(message)s')
    import config
    check_config_exists()
    config.set_config(DEF_CONFIG_NAME)
    from consoleserver import console_server
    console_server()
    _log.info("Starting twisted reactor")
    reactor.run()

if __name__ == '__main__':
    main()
