# -*- coding: utf-8 -*-
# author: Ethosa


def create_button(button_type="text", color="primary", **kwargs):
    """
    Creates a new Button object.

    Keyword Arguments:
        button_type {str} -- button type. (default: {"text"})
        color {str} -- button color. (default: {"primary"})
            Can be "primary", "secondary", "positive" or "negative".
    """
    obj = {}
    if button_type == "text":
        obj["color"] = color
    obj["action"] = kwargs
    obj["action"]["type"] = button_type
    return obj
