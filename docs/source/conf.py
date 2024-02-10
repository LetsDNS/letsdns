# See https://www.sphinx-doc.org/en/master/usage/configuration.html
# vim:ts=4:sw=4:et
import os
import sys

from letsdns import VERSION

sys.path.insert(0, os.path.abspath('..'))

author = 'Ralph Seichter'
language = 'en'
project = 'LetsDNS'
project_copyright = '2022-2024 Ralph Seichter'

# The short X.Y version
version = 'latest'
# The full version, including alpha/beta/rc tags
release = VERSION

exclude_patterns = [
    ".DS_Store",
    "_build",
    "build",
]
extensions = ['sphinx.ext.autodoc']

html_favicon = 'favicon.ico'
html_static_path = ['_static']
html_last_updated_fmt = '%Y-%m-%d'
html_theme = 'sphinx_rtd_theme'
html_title = 'LetsDNS'
