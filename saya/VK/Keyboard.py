# -*- coding: utf-8 -*-
# author: Ethosa

import json


class Keyboard(dict):
    def __init__(self, one_time=False, inline=False, other_keyboard=None):
        if other_keyboard:
            self.__init__(other_keyboard["one_time"], other_keyboard["inline"])
            self["buttons"] = other_keyboard["buttons"][:]
        else:
            self["inline"] = inline
            self["one_time"] = one_time
            self["buttons"] = [[]]
        if self["inline"]:
            self.max_size = (3, 3)
            del self["one_time"]
        else:
            self.max_size = (4, 10)

    def add(self, button):
        if len(self["buttons"]) < self.max_size[1]:
            if len(self["buttons"][-1]) < self.max_size[0]:
                if button["action"]["type"] == "text":
                    self["buttons"][-1].append(button)
                else:
                    if len(self["buttons"][-1]) > 0:
                        self.add_line()
                    self["buttons"][-1].append(button)

    def add_line(self):
        if len(self["buttons"]) < self.max_size[1]:
            self["buttons"].append([])

    def compile(self):
        return json.dumps(self)
