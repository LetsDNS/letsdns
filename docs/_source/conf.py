# Configuration file for the Sphinx documentation builder.
#
# This file only contains a selection of the most common options. For a full
# list see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html
import os
import sys

sys.path.insert(0, os.path.abspath('..'))

# -- Project information -----------------------------------------------------

project = 'LetsDNS'
copyright = '2022 Ralph Seichter'
author = 'Ralph Seichter <r@letsdns.org>'

# The short X.Y version
version = '0.1'
# The full version, including alpha/beta/rc tags
release = '0.1.dev2'

# Add any Sphinx extension module names here, as strings. They can be
# extensions coming with Sphinx (named 'sphinx.ext.*') or your custom
# ones.
extensions = [
    'sphinx.ext.autodoc',
    'sphinx.ext.napoleon',
]

# List of patterns, relative to source directory, that match files and
# directories to ignore when looking for source files.
# This pattern also affects html_static_path and html_extra_path.
exclude_patterns = [
    ".DS_Store",
    "_build",
]

# Add any paths that contain templates here, relative to this directory.
templates_path = ['_templates']

# Options for HTML output
html_static_path = ['_static']
html_theme = 'alabaster'
