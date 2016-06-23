import subprocess

from mako.template import Template
from mako.lookup import TemplateLookup
from plim import preprocessor

from .base import SourceFileTransformer
from .util import split_markup


class PageTransformer(SourceFileTransformer):
    input_ext = None
    output_ext = '.html'
    mime_type = 'text/html'
    template_imports = ['from jingtai.assets import stylesheet, script']

    def __init__(self, site):
        super(PageTransformer, self).__init__(site)
        self.lookup = TemplateLookup(
            directories=[str(self.site.template_dir)],
            preprocessor=preprocessor,
            imports=self.template_imports + site.template_imports)
