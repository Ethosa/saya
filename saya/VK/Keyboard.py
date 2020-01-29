# -*- coding: utf-8 -*-
# author: Ethosa

from json import dumps


class Keyboard(dict):
    def __init__(self, one_time=False, inline=False, other_keyboard=None):
        """Initializes Keyboard object.

        if other_keyboard is another Keyboard object, then params of this keyboard copied from other Keyboard object.

        Keyword Arguments:
            one_time {bool} -- Hides keyboard after the first answer if True. (default: {False})
            inline {bool} -- Shows keyboard inside the message, if True. (default: {False})
            other_keyboard {Keyboard} -- other Keyboard object. (default: {None})
        """
        if other_keyboard:
            self["one_time"] = other_keyboard["one_time"]
            self["inline"] = other_keyboard["inline"]
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
        """Adds a new button in keyboard.

        Arguments:
            button {Button} -- Button object.
        """
        if len(self["buttons"]) < self.max_size[1]:
            if len(self["buttons"][-1]) < self.max_size[0]:
                if button["action"]["type"] == "text":
                    self["buttons"][-1].append(button)
                else:
                    if len(self["buttons"][-1]) > 0:
                        self.add_line()
                    self["buttons"][-1].append(button)

    def add_line(self):
        """Adds a new line in the keyboard, if possible."""
        if len(self["buttons"]) < self.max_size[1]:
            self["buttons"].append([])

    def compile(self):
        """Compiles keyboard for sending it in the message.

        Returns:
            dict -- dictionary object for message sending.
        """
        return dumps(self)
