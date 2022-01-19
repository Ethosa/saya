# -*- coding: utf-8 -*-
# author: Ethosa
from typing import NoReturn, Dict, Any
from json import dumps


class Keyboard(dict):
    # noinspection PyMissingConstructor
    def __init__(
            self,
            one_time: bool = False,
            inline: bool = False,
            other_keyboard = None
    ):
        """Initializes Keyboard object.

        if other_keyboard is another Keyboard object, then params of this keyboard copied from other Keyboard object.

        :param one_time: Hides keyboard after the first answer if True.
        :param inline: Shows keyboard inside the message, if True.
        :param other_keyboard: other Keyboard object.
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

    def add(
            self,
            button: Dict[str, Any]
    ) -> NoReturn:
        """Adds a new button in keyboard.

        :param button: Button object.
        """
        if len(self["buttons"]) < self.max_size[1]:
            if len(self["buttons"][-1]) < self.max_size[0]:
                if button["action"]["type"] == "text":
                    self["buttons"][-1].append(button)
                else:
                    if len(self["buttons"][-1]) > 0:
                        self.add_line()
                    self["buttons"][-1].append(button)

    def add_line(self) -> NoReturn:
        """Adds a new line in the keyboard, if possible."""
        if len(self["buttons"]) < self.max_size[1]:
            self["buttons"].append([])

    def compile(self) -> str:
        """Compiles keyboard for sending it in the message.
        """
        return dumps(self)
