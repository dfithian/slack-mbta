import web
import config
import logging
from const import ROUTE_ENDPOINT
from messaging_thread import MessagingThread

log = logging.getLogger(__name__)

class get_route:
    def GET(self):
        MessagingThread(ROUTE_ENDPOINT, web.input()).run()
        return ''

class SlackApp(web.application):
    def run(self, host, port, *middleware):
        log.info("starting web application with address {0}:{1}".format(host, port))
        func = self.wsgifunc(*middleware)
        return web.httpserver.runsimple(func, server_address=(host, port))

def start_app():
    urls = (
        '/%s' % (ROUTE_ENDPOINT), 'get_route'
    )
    app = SlackApp(urls, globals())
    app.run(config.config['host'], config.config['port'])
