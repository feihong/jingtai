import subprocess

from mako.template import Template
from mako.lookup import TemplateLookup
from plim import preprocessor

from .base import SourceFileTransformer, register_transformer
from .util import split_markup


IMPORTS = [
    'from jingtai.assets import stylesheet, script'
]


@register_transformer
class PlimTransformer(SourceFileTransformer):
    input_ext = '.html'
    output_ext = '.html'
    mime_type = 'text/html'

    def __init__(self, site):
        super(PlimTransformer, self).__init__(site)
        self.lookup = TemplateLookup(
            directories=[str(self.site.template_dir)],
            preprocessor=preprocessor)

    def transform(self, src):
        ctx, text = split_markup(src.read_text())
        ctx['BASE'] = self.site.base_url
        tmpl = Template(
            text=text,
            lookup=self.lookup,
            preprocessor=preprocessor,
            imports=IMPORTS)
        return tmpl.render(**ctx)
