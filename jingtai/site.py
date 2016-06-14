from .compat import Path
from .server import start_server, send
from .watcher import start_watcher


class Site(object):
    _current = None

    def __init__(self, base_url):
        self.base_url = base_url
        self.site_dir = Path.cwd() / 'site'
        self.build_dir = Path.cwd() / 'build'
        self.template_dir = Path.cwd() / 'templates'
        self.watch_list = []

        Site._current = self

    @classmethod
    def current(cls):
        return Site._current

    def serve(self, port=8000):
        watcher = start_watcher(self.watch_list)
        start_server(self, port)
        watcher.stop()

    def serve_build(self, port=8000):
        pass

    def watch(self, dirname):
        self.watch_list.append(dirname)

    def build(self):
        self.clean()
        for src in self.site_dir.rglob('*?.*'):
            dest_dir = self.build_dir / src.relative_to(self.site_dir).parent
            dest_file = self.copy_or_generate(src, dest_dir)
            print(dest_file)

    def clean(self):
        if self.build_dir.is_dir():
            run('rm -rf %s/*' % self.build_dir)

    def publish(self):
        self.build()
        run('ghp-import -n -p %s' % self.build_dir)
