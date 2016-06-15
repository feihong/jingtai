import markdown2
from mako.template import Template
from mako.lookup import TemplateLookup
from plim import preprocessor

from .base import SourceFileTransformer, register_transformer
from .util import split_markup


EXTRAS = ['fenced-code-blocks', 'footnotes']


@register_transformer
class MarkdownTransformer(SourceFileTransformer):
    input_ext = '.md'
    output_ext = '.html'
    mime_type = 'text/html'

    def __init__(self, site):
        super(MarkdownTransformer, self).__init__(site)
        self.lookup = TemplateLookup(
            directories=[str(self.site.template_dir)],
            preprocessor=preprocessor)

    def transform(self, src):
        ctx, text = split_markup(src.read_text())
        ctx['BASE'] = self.site.base_url
        text = '<%inherit file="base.html" />\n\n' + self.to_html(text)
        # Note that we don't use the plim preprocessor here, because arbitrary
        # HTML confuses the plim parser.
        tmpl = Template(
            text=text,
            lookup=self.lookup)
        return tmpl.render(**ctx)

    def to_html(self, text):
        return markdown2.markdown(text, extras=EXTRAS)
