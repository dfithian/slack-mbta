import logging
import time
import threading
from config import Config
from output import OutputFactory
from transaction import TransactionContext
from Queue import Queue

# read queue every 2 seconds and process everything in there
log = logging.getLogger(__name__)
def config():
    return Config.instance()
def outputter():
    return OutputFactory.get_outputter(config())
def transaction_flow(txn_context, config, outputter):
    txn_context.do_transaction()
    return outputter.format(txn_context.request, txn_context.reply)

class SlackMessagingThread(threading.Thread):
    queue = Queue()
    def __init__(self, *args, **kwargs):
        super(SlackMessagingThread, self).__init__(*args, **kwargs)
    def run(self):
        while 1:
            time.sleep(2)
            while not SlackMessagingThread.queue.empty():
                try:
                    (constructor, input_params) = SlackMessagingThread.queue.get()
                    txn_context_mbta = constructor(config(), input_params)
                    payload = transaction_flow(txn_context_mbta, config(), outputter())
                    txn_context_slack = TransactionContext.SLACK_TXN_CONTEXT(config(), payload)
                    txn_context_slack.do_transaction()
                except Exception:
                    log.exception('Got exception processing payload {0}'.format(payload_to_process))

