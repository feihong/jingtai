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

    def build(self, src, dest_dir):
        dest_file = self.get_dest_file(src, dest_dir)
        cmd = ['stylus', '-o', str(dest_file), str(src)]
        return subprocess.call(cmd)
