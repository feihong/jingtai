import sys
import os
import re
from setuptools import setup, find_packages


if sys.argv[-1] == 'publish':
    os.system('python setup.py sdist upload')
    sys.exit()


requires = [
    'Plim',
    'watchdog',
    'invoke',
    'tornado',
]
if sys.version_info[0] == 2:
    requires.extend(['futures', 'pathlib2'])


with open('jingtai/__init__.py') as fp:
    version = re.search(r'^__version__\s*=\s*[\'"]([^\'"]*)[\'"]',
                        fp.read(), re.MULTILINE).group(1)

with open('README.rst') as fp:
    readme = fp.read()


setup(
    name='jingtai',
    version=version,
    description='Static site generator for coders who love minimal syntaxes',
    long_description=readme,
    author='Feihong Hsu',
    author_email='feihong.hsu@gmail.com',
    url='https://github.com/feihong/jingtai',
    packages=find_packages(),
    package_data={'': '*.html'},
    install_requires=requires,
    license='Apache 2.0',
    zip_safe=False,
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Natural Language :: English',
        'License :: OSI Approved :: Apache Software License',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: Implementation :: CPython',
        'Programming Language :: Python :: Implementation :: PyPy',
    ],
)
