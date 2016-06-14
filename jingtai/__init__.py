__title__ = 'jingtai'
__version__ = '0.1.0'
__author__ = 'Feihong Hsu'
__license__ = 'Apache 2.0'
__copyright__ = 'Copyright 2016 Feihong Hsu'
__all__ = ['Site']


from server import start_server, send
from watcher import start_watcher

from .compat import Path


def create_project(name):
    Path.mkdir(name)
    # tbd


class Site(object):
    def __init__(self, base_url, site_dir=None, build_dir=None):
        self.base_url = base_url
        if site_dir is None:
            self.site_dir = Path.cwd() / 'site'
        else:
            self.site_dir = Path(site_dir)
        if build_dir is None:
            self.build_dir = Path.cwd() / 'build'
        else:
            self.build_dir = Path(build_dir)

        self.watch_list = []

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
