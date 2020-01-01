# -*- coding: utf-8 -*-
# author: Ethosa


class PushEvent(dict):
    def __init__(self, **kwargs):
        """More convenient writing your own events

        Arguments:
            **kwargs -- event info

        Usage:
            custom_event = PushEvent(type="custom_type", info="hello world")
        """
        for key in kwargs:
            self[key] = kwargs[key]
