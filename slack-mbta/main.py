import argparse
import logging
from config import Config
from rest_api_thread import RestAPIThread
from slack_messaging_thread import SlackMessagingThread

logging.basicConfig(level=logging.DEBUG)
parser = argparse.ArgumentParser(description="Get MBTA info", epilog="(c) 2015 Dan Fithian")
parser.add_argument("-c", dest="config_file", type=str, help="provide a config file")

opts = parser.parse_args()
config = Config(opts.config_file)
SlackMessagingThread(config).start()
RestAPIThread(config).start()
