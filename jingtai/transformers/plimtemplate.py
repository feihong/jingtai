import subprocess

from mako.template import Template
from plim import preprocessor

from .base import register_transformer
from .page import PageTransformer
from .util import split_markup


@register_transformer
class PlimTransformer(PageTransformer):
    input_ext = '.plim'

    def transform(self, src):
        ctx, text = split_markup(src.read_text())
        ctx.update(
            BASE=self.site.base_url,
            PATH=src,
            MODE=self.site.mode,
        )
        tmpl = Template(
            text=text,
            lookup=self.lookup,
            preprocessor=preprocessor,
            imports=self.template_imports + self.site.template_imports)
        return tmpl.render(**ctx)
