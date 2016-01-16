import logging
import threading
from transaction import make_mbta_context, make_slack_context

log = logging.getLogger(__name__)
class MessagingThread(threading.Thread):
    def __init__(self, endpoint, params, *args, **kwargs):
        self.endpoint = endpoint
        self.params = params
        super(MessagingThread, self).__init__(*args, **kwargs)
    def run(self):
        try:
            mbta_context = make_mbta_context(self.endpoint, self.params)
            mbta_context.do_transaction()
            slack_context = make_slack_context(mbta_context, self.params)
            slack_context.do_transaction()
        except Exception:
            log.exception('got exception running messaging thread')
