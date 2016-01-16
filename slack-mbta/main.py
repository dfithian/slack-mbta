import json
import argparse
import logging
import config
from api import start_app

logging.basicConfig(level=logging.DEBUG)
log = logging.getLogger(__name__)
parser = argparse.ArgumentParser(description="Get MBTA info", epilog="(c) 2015 Dan Fithian")
parser.add_argument("-c", dest="config_file", type=str, help="provide a config file")

opts = parser.parse_args()
try:
    json = json.loads(open(opts.config_file, 'r').read())
    setattr(config, 'config', json)
    start_app()
except Exception:
    log.exception('failed to load config due to exception')
