import subprocess

from mako.template import Template
from mako.lookup import TemplateLookup
from plim import preprocessor

from .base import SourceFileTransformer, register_transformer
from .util import split_markup


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
        tmpl = Template(
            text=text,
            lookup=self.lookup,
            preprocessor=preprocessor)
        return tmpl.render(BASE=self.site.base_url, **ctx)
