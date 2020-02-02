# -*- coding: utf-8 -*-
# author: Ethosa

from json import dumps


class Template(dict):
    def __init__(self, ttype="carousel"):
        """
        Creates a Template object.

        Keyword Arguments:
            ttype {str} -- template type. (default: {"carousel"})
        """
        self["type"] = ttype
        self["elements"] = []

    def add(self, element):
        """Adds new element in template.

        Arguments:
            element {TemplateElement}
        """
        if len(self["elements"]) < 10:
            self["elements"].append(element)

    def compile(self):
        """Compiles Template for sendng in the message.

        Returns:
            dict -- compiled Template.
        """
        return dumps(self)
