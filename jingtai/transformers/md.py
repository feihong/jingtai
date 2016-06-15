import markdown2

from .base import SourceFileTransformer, register_transformer


extras=['fenced-code-blocks', 'footnotes']


@register_transformer
class MarkdownTransformer(SourceFileTransformer):
    input_ext = '.md'
    output_ext = '.html'
    mime_type = 'text/html'

    def transform(self, src):
        return markdown2.markdown(src.read_text(), extras)
