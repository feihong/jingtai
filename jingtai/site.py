import shutil

from .compat import Path
from .server import start_server, send
from .watcher import start_watcher
from .transformers import init_transformers, transformers


class Site(object):
    def __init__(self, base_url):
        self.base_url = base_url
        self.site_dir = Path.cwd() / 'site'
        self.build_dir = Path.cwd() / 'build'
        self.template_dir = Path.cwd() / 'templates'
        self.watch_list = []

    @classmethod
    def instance(cls):
        return Site._instance

    def serve(self, port=8000):
        init_transformers(self)
        watcher = start_watcher(self.watch_list)
        start_server(self, port)
        watcher.stop()

    def serve_build(self, port=8000):
        pass

    def watch(self, dirname):
        self.watch_list.append(dirname)

    def build(self):
        init_transformers(self)
        self.clean()
        for src in self.site_dir.rglob('*?.*'):
            transformer = transformers.get(src.suffix)
            if transformer is not None:
                transformer.build(src)
            else:
                shutil.copy(
                    str(src),
                    str(self.build_dir / src.relative_to(self.site_dir))
                )

    def clean(self):
        if self.build_dir.is_dir():
            run('rm -rf %s/*' % self.build_dir)

    def publish(self):
        self.build()
        run('ghp-import -n -p %s' % self.build_dir)
