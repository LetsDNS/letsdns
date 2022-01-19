#!/usr/bin/env python

from livereload import Server
from livereload import shell


def watch(s: Server, what: str) -> None:
    s.watch(f'source/{what}', shell('make html'), delay=2)


def serve() -> None:
    s = Server()
    watch(s, '*.rst')
    watch(s, '_static/*')
    watch(s, '_templates/*')
    s.serve(root='build/html')


if __name__ == '__main__':
    serve()
