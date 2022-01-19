# -*- coding: utf-8 -*-
# author: Ethosa
from typing import NoReturn, Dict, Any
from json import dumps


class Template(dict):
    # noinspection PyMissingConstructor
    def __init__(
            self,
            ttype: str = "carousel"
    ):
        """Creates a Template object.

        :param ttype: template type.
        """
        self["type"] = ttype
        self["elements"] = []

    def add(
            self,
            element: Dict[str, Any]
    ) -> NoReturn:
        """Adds new element in template.

        :param element: template element
        """
        if len(self["elements"]) < 10:
            self["elements"].append(element)

    def compile(self) -> str:
        """Compiles Template for sendng in the message.
        """
        return dumps(self)
