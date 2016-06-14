from tornado import gen, iostream
from tornado.web import Application, RequestHandler
from tornado.websocket import WebSocketHandler
from tornado.ioloop import IOLoop
from mako.template import Template
from mako.lookup import TemplateLookup
import plim
import stylus

from .compat import Path
from .transformers import get_transformer


here = Path(__file__).parent
site = None


def start_server(site_, port):
    global site, app
    settings = dict(
        debug=True,
        # autoreload=True,
    )
    app = Application([
        (r'/__reload.js/', ReloadJSHandler),
        (r'/__reload__/', ReloadHandler),
        (r'/(.*)', NoCacheFileHandler),
    ], **settings)
    site = site_
    app.sockets = set()
    app.listen(port)

    loop = IOLoop.current()
    send.loop = loop
    send.sockets = app.sockets
    loop.start()


class ReloadJSHandler(RequestHandler):
    def get(self):
        self.set_header('Content-Type', 'text/javascript')
        reload_file = here / 'reload.js'
        self.write(reload_file.read_bytes())


class ReloadHandler(WebSocketHandler):
    def open(self):
        self.application.sockets.add(self)

    def on_close(self):
        self.application.sockets.remove(self)


class NoCacheFileHandler(RequestHandler):
    @gen.coroutine
    def get(self, path):
        self.set_header('Cache-Control', 'no-store')

        filepath = site.site_dir / path
        if filepath.is_dir():
            filepath = filepath / 'index.html'

        if not filepath.exists():
            self.clear()
            self.set_status(404)
            self.finish((site.site_dir / '404.html').read_bytes())

        content = get_content(filepath)
        for chunk in content:
            try:
                self.write(chunk)
                yield self.flush()
            except iostream.StreamClosedError:
                return


class SendCallable:
    """
    A callable object that is used to communicate with the browser.

    """

    def __init__(self):
        self.loop = None
        self.sockets = None

    def __call__(self, obj):
        """
        It is safe to call this method from outside the main thread that is
        running the Tornado event loop.

        """
        if not self.loop:
            return
        data = json.dumps(obj)
        self.loop.add_callback(self._send, data)

    def _send(self, data):
        "Write the given data to all connected websockets."
        for socket in self.sockets:
            socket.write_message(data)


send = SendCallable()


def get_content(path):
    with path.open('rb') as fp:
        remaining = None
        while True:
            chunk_size = 64 * 1024
            if remaining is not None and remaining < chunk_size:
                chunk_size = remaining
            chunk = fp.read(chunk_size)
            if chunk:
                if remaining is not None:
                    remaining -= len(chunk)
                yield chunk
            else:
                if remaining is not None:
                    assert remaining == 0
                return
