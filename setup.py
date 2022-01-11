"""
Copyright (c) 2022 Ralph Seichter.

This file is part of LetsDNS.

LetsDNS is free software: you can redistribute it and/or modify it under the terms of the GNU General Public License
as published by the Free Software Foundation, either version 3 of the License, or (at your option) any later version.

LetsDNS is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty
of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for more details.

You should have received a copy of the GNU General Public License along with LetsDNS. If not, see
<https://www.gnu.org/licenses/>.
"""
import setuptools

from letsdns import HOMEPAGE
from letsdns import IDENTIFIER
from letsdns import VERSION

with open('README.md', 'r') as f:
    readme = f.read()

setuptools.setup(
    name=IDENTIFIER,
    version=VERSION,
    author='Ralph Seichter',
    author_email='r@letsdns.org',
    description='Mail client autoconfiguration service',
    long_description=readme,
    long_description_content_type='text/markdown',
    url=HOMEPAGE,
    project_urls={
        'Source': 'https://gitlab.com/letsdns/letsdns',
        'Tracker': 'https://gitlab.com/letsdns/letsdns/-/issues',
    },
    packages=setuptools.find_packages(),
    classifiers=[
        'Development Status :: 1 - Planning',
        'License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3',
    ],
    install_requires=[
        'dnspython>=2.1.0',
    ],
    python_requires='>=3.7',
)
