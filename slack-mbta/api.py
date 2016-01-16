import web
import config
import logging
from const import ROUTE_ENDPOINT, ALERTS_ENDPOINT, ALERT_ENDPOINT
from messaging_thread import MessagingThread

log = logging.getLogger(__name__)

class get_route:
    def GET(self):
        MessagingThread(ROUTE_ENDPOINT, web.input()).run()
        return ''

class get_alert:
    def GET(self):
        MessagingThread(ALERT_ENDPOINT, web.input()).run()
        return ''

class get_alerts:
    def GET(self):
        MessagingThread(ALERTS_ENDPOINT, web.input()).run()
        return ''

class SlackApp(web.application):
    def run(self, host, port, *middleware):
        log.info("starting web application with address {0}:{1}".format(host, port))
        func = self.wsgifunc(*middleware)
        return web.httpserver.runsimple(func, server_address=(host, port))

def start_app():
    urls = (
        '/%s' % (ROUTE_ENDPOINT), 'get_route',
        '/%s' % (ALERT_ENDPOINT), 'get_alert',
        '/%s' % (ALERTS_ENDPOINT), 'get_alerts'
    )
    app = SlackApp(urls, globals())
    app.run(config.config['host'], config.config['port'])
