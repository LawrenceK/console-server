import logging
import logging.config
_log = logging.getLogger(__name__)
import os
import os.path
from twisted.internet import reactor

DEF_CONFIG_NAME = 'config.ini'
DEF_LOGGING_NAME = 'logging.ini'
CONFIG_FILENAME = '/etc/consoleserver/config.ini'
LOGGING_FILENAME = '/etc/consoleserver/logging.ini'

def check_exists(srcName, destName):
    if not os.path.exists(destName):
        _log.info("Copying default config file %s", destName)
        if not os.path.exists(os.path.dirname(destName)):
            os.mkdir(os.path.dirname(destName))
        import shutil
        shutil.copy2(os.path.join(os.path.dirname(os.path.abspath(__file__)), srcName), destName)

def check_config_exists():
    check_exists(DEF_CONFIG_NAME, CONFIG_FILENAME)
    check_exists(DEF_LOGGING_NAME, LOGGING_FILENAME)

def main():
    logging.basicConfig(level=logging.WARNING,
                        format='%(asctime)s %(levelname)s [%(funcName)s] %(message)s')
    import config
#    check_config_exists()
#    logging.config.fileConfig(LOGGING_FILENAME)
    logging.config.fileConfig(config.find_file(DEF_LOGGING_NAME))
#    config.set_config(CONFIG_FILENAME)
    config.set_config(config.find_file(DEF_CONFIG_NAME))
    from consoleserver import console_server
    console_server()
    _log.info("Starting twisted reactor")
    reactor.run()

if __name__ == '__main__':
    main()
