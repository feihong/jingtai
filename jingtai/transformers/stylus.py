import subprocess
from .base import SourceFileTransformer, register_transformer


@register_transformer
class StylusTransformer(SourceFileTransformer):
    input_ext = '.styl'
    output_ext = '.css'
    mime_type = 'text/css'

    def transform(self, src):
        cmd = ['stylus', '-p', str(src)]
        return subprocess.check_output(cmd)

    def build(self, src):
        cmd = ['stylus', str(src), '-o', str(self.get_dest_file(src))]
        return subprocess.call(cmd)
