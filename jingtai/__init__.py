__title__ = 'jingtai'
__version__ = '0.1.0'
__author__ = 'Feihong Hsu'
__license__ = 'Apache 2.0'
__copyright__ = 'Copyright 2016 Feihong Hsu'
__all__ = ['Site']


from .site import Site
from .compat import Path


def create_project(name):
    Path.mkdir(name)
    # tbd
