import logging
import time
import threading
from config import Config
from transaction import TransactionContext
from Queue import Queue

# read queue every 2 seconds and process everything in there
log = logging.getLogger(__name__)
class SlackMessagingThread(threading.Thread):
    queue = Queue()
    def __init__(self, *args, **kwargs):
        super(SlackMessagingThread, self).__init__(*args, **kwargs)
    def run(self):
        while 1:
            time.sleep(2)
            while not SlackMessagingThread.queue.empty():
                try:
                    payload_to_process = SlackMessagingThread.queue.get()
                    txn_context = TransactionContext.SLACK_TXN_CONTEXT(Config.instance(), payload_to_process)
                    txn_context.do_transaction()
                except Exception:
                    log.exception('Got exception processing payload {0}'.format(payload_to_process))

