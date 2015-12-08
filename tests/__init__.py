# coding=utf-8
import sys

PYPY = '__pypy__' in sys.builtin_module_names
PY27 = sys.version_info[0:2] == (2, 7) and not PYPY


def is_int(p_object):
    return isinstance(p_object, int)
