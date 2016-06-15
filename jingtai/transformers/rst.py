from docutils.core import publish_parts

from .base import SourceFileTransformer, register_transformer


@register_transformer
class ReStructuredTextTransformer(SourceFileTransformer):
    input_ext = '.rst'
    output_ext = '.html'
    mime_type = 'text/html'

    def transform(self, src):
        result = publish_parts(
            src.read_text(),
            writer_name='html',
            settings_overrides={'initial_header_level': 2})['html_body']
        # Get rid of the outer div.
        return result[22:-7]
