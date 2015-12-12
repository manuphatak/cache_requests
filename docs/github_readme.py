#!/usr/bin/env python3
# coding=utf-8
from datetime import datetime
from functools import partial, reduce
from os.path import dirname, realpath, join


# CONFIG UTILS
# ----------------------------------------------------------------------------
def path(*args):
    return realpath(join(*args))


# CONFIG
# ----------------------------------------------------------------------------
DOCS = partial(path, dirname(__file__))
SOURCE = partial(DOCS, 'source')
PROJECT = partial(DOCS, '..')
OUT_FILE = PROJECT('README.rst')

comment_line = """.. This document was procedurally generated by %s on %s"""
HEADER = comment_line % (__file__, datetime.now().strftime('%c'))


def include_documents(*_):
    yield read_text(HEADER)
    yield read_source('readme_title.rst')
    yield read_source('readme_features.rst')
    yield read_source('installation.rst')
    yield read_source('usage.rst')
    yield read_source('readme_credits.rst')


# PRE CONFIGURED PARTIALS
# ----------------------------------------------------------------------------
def read_source(file_name):
    # noinspection PyCompatibility
    yield from read_file(SOURCE(file_name))


def write_out(lines):
    # noinspection PyCompatibility
    yield from write_file(OUT_FILE, lines)


# PROCESS PIPELINE
# ----------------------------------------------------------------------------
def read_file(file_name):
    with open(file_name) as f:
        # noinspection PyCompatibility
        yield from f


def read_text(text):
    # noinspection PyCompatibility
    yield from text.splitlines(True)


def concatenate(file_iterators):
    for file_iterator in file_iterators:
        # noinspection PyCompatibility
        yield from file_iterator
        yield '\n\n'


def sanitize(lines):
    # optional text manipulation.
    for line in lines:
        yield line


def write_file(file_name, lines):
    with open(file_name, 'w') as f:
        for line in lines:
            yield f.write(line)


def notify(lines):
    print('Writing README.rst ', end='')
    for i, line in enumerate(lines):
        if i % 5 == 0:
            print('.', end='')

        yield line

    print(' Done!')


# SCRIPT UTILS
# ----------------------------------------------------------------------------
def pipeline(steps, initial=None):
    def apply(result, step):
        # noinspection PyCompatibility
        yield from step(result)

    # noinspection PyCompatibility
    yield from reduce(apply, steps, initial)


# RUN SCRIPT
# ----------------------------------------------------------------------------
if __name__ == '__main__':
    process = include_documents, concatenate, sanitize, write_out, notify
    list(pipeline(process))