# -*- coding: utf-8 -*-
# author: Ethosa


def deprecated(version):
    def _decorator(function):
        def call(*args, **kwargs):
            print("[WARNING]: method \"%s\" is deprecated in version %s, please remove it from code." % (
                    function.__name__,
                    version
                )
            )
            return function(*args, **kwargs)
        return call
    return _decorator
