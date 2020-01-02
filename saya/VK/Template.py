# -*- coding: utf-8 -*-
# author: Ethosa

import json


class Template(dict):
    def __init__(self, ttype="carousel"):
        self["type"] = ttype
        self["elements"] = []

    def add(self, element):
        """add new element in template

        Arguments:
            element {TemplateElement}
        """
        if len(self["elements"]) < 10:
            self["elements"].append(element)

    def compile(self):
        return json.dumps(self)
