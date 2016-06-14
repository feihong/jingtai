

__all__ = ['get_transformer', 'SourceFileTransformer', 'register_transformer']


from .base import SourceFileTransformer, register_transformer, transformers


def get_transformer(src_file):
    for transformer in transformers:
        if src_file.suffix == transformer.input_ext:
            return transformer
    return None
