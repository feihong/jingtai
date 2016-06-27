import shutil

from invoke import run

from .compat import Path
from .server import start_server, send, start_static_server
from .watcher import start_watcher
from .transformers import init_transformers, transformers
from . import assets


class Site(object):
    def __init__(self, base_url, template_imports=None):
        self.base_url = base_url
        self.site_dir = Path.cwd() / 'site'
        self.build_dir = Path.cwd() / 'build'
        self.template_dir = Path.cwd() / 'templates'
        self.watch_list = []
        self.mode = 'serve'
        self.template_imports = template_imports if template_imports else []

    @classmethod
    def instance(cls):
        return Site._instance

    def serve(self, port=8000):
        init_transformers(self)
        watcher = start_watcher(self.watch_list)
        start_server(self, port)
        watcher.stop()

    def serve_build(self, port=8000):
        start_static_server(self, port)

    def watch(self, path):
        self.watch_list.append(Path(path).absolute())

    def build(self):
        init_transformers(self)
        self.clean()

        self.mode = assets.mode = 'build'
        for root, dirs, files in path_walk(self.site_dir):
            for src in files:
                print(src)
                dest_dir = self.get_make_dest_dir(src)
                transformer = transformers.get(src.suffix)
                if transformer is not None:
                    transformer.build(src, dest_dir)
                else:
                    shutil.copy(str(src), str(dest_dir))

    def clean(self):
        if self.build_dir.is_dir():
            run('rm -rf %s/*' % self.build_dir)

    def publish(self):
        self.build()
        run('ghp-import -n -p %s' % self.build_dir)

    def get_make_dest_dir(self, src):
        dest = self.build_dir / src.relative_to(self.site_dir)
        dest_dir = dest.parent
        if not dest_dir.exists():
            dest_dir.mkdir(parents=True)
        return dest_dir


def path_walk(top, topdown=False, followlinks=False):
    """
    Source: http://ominian.com/2016/03/29/os-walk-for-pathlib-path/

    """
    names = list(top.iterdir())

    dirs = (node for node in names if node.is_dir() is True)
    nondirs = (node for node in names if node.is_dir() is False)

    if topdown:
        yield top, dirs, nondirs

    for name in dirs:
        if followlinks or name.is_symlink() is False:
            for x in path_walk(name, topdown, followlinks):
                yield x

    if topdown is not True:
        yield top, dirs, nondirs
