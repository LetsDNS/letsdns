# Configuration file for the Sphinx documentation builder.
# See https://www.sphinx-doc.org/en/master/usage/configuration.html
import os
import sys

from letsdns import VERSION

sys.path.insert(0, os.path.abspath('..'))

# -- Project information -----------------------------------------------------

project = 'LetsDNS'
project_copyright = '2022 Ralph Seichter'
author = 'Ralph Seichter'

# The short X.Y version
version = 'latest'
# The full version, including alpha/beta/rc tags
release = VERSION

extensions = [
    'sphinx.ext.autodoc',
    'sphinx.ext.napoleon',
]

# List of patterns, relative to source directory, that match files and
# directories to ignore when looking for source files. This pattern also
# affects html_static_path and html_extra_path.
exclude_patterns = [
    ".DS_Store",
    "_build",
]

# Add any paths that contain templates here, relative to this directory.
templates_path = ['_templates']

# Options for HTML output.
html_static_path = ['_static']
html_theme = 'sphinx_rtd_theme'
