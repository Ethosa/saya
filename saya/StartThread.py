# -*- coding: utf-8 -*-
# author: Ethosa

from threading import Thread


class StartThread(Thread):
    def __init__(self, callable_obj, *args, **kwargs):
        self.callable_obj = callable_obj
        self.args = args
        self.kwargs = kwargs
        Thread.__init__(self)

    def run(self):
        self.callable_obj(*self.args, **self.kwargs)
