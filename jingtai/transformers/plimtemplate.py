import subprocess

from mako.template import Template
from mako.lookup import TemplateLookup
from plim import preprocessor

from .base import SourceFileTransformer, register_transformer


@register_transformer
class PlimTransformer(SourceFileTransformer):
    input_ext = '.html'
    output_ext = '.html'
    mime_type = 'text/html'

    def transform(self, src):
        tmpl = Template(
            text=src.read_text(),
            lookup=self.lookup,
            preprocessor=preprocessor)
        return tmpl.render()

    @property
    def lookup(self):
        res = getattr(self, '_lookup', None)
        if res is None:
            self._lookup = TemplateLookup(
                directories=[str(self.site.template_dir)],
                preprocessor=preprocessor)
        return self._lookup
