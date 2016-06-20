__title__ = 'jingtai'
__version__ = '0.1.1'
__author__ = 'Feihong Hsu'
__license__ = 'Apache 2.0'
__copyright__ = 'Copyright 2016 Feihong Hsu'
__all__ = ['Site']


import shutil
from .site import Site
from .compat import Path


def create_project(name):
    resources = Path(__file__).parent / 'resources'

    root = Path(name)
    root.mkdir()

    (root / 'tasks.py').write_text(
        (resources / 'tasks.py').read_text() % {'project_name': name}
    )

    site = root / 'site'
    site.mkdir()

    shutil.copy(str(resources / '404.html'), str(site))
    shutil.copy(str(resources / 'index.html'), str(site))

    templates = root / 'templates'

    shutil.copy(str(resources / 'base.plim'), str(templates))
