# -*- coding: utf-8 -*-
# author: Ethosa


def deprecated(version, removed_version):
    def _decorator(function):
        def call(*args, **kwargs):
            print(
                ("[WARNING]: method \"%s\" is deprecated in "
                 "version [%s], please remove it from code. "
                 "In version [%s] this method will be removed."
                 ) % (function.__qualname__, version, removed_version)
            )
            return function(*args, **kwargs)
        return call
    return _decorator
