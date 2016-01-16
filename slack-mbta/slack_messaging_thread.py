import logging
import time
import threading
from transaction import TransactionContext
from Queue import Queue

log = logging.getLogger(__name__)
# read queue every 2 seconds and process everything in there
def transaction_flow(txn_context, config):
    txn_context.do_transaction()
    return config.outputter.format(txn_context.request, txn_context.reply)

class SlackMessagingThread(threading.Thread):
    queue = Queue()
    def __init__(self, config, *args, **kwargs):
        self.config = config
        super(SlackMessagingThread, self).__init__(*args, **kwargs)
    def run(self):
        while 1:
            time.sleep(2)
            while not SlackMessagingThread.queue.empty():
                try:
                    (constructor, input_params) = SlackMessagingThread.queue.get()
                    txn_context_mbta = constructor(self.config, input_params)
                    payload = transaction_flow(txn_context_mbta, self.config)
                    txn_context_slack = TransactionContext.SLACK_TXN_CONTEXT(self.config, payload)
                    txn_context_slack.do_transaction()
                except Exception:
                    log.exception('Got exception processing payload {0}'.format(payload))

