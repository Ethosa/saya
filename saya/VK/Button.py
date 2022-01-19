# -*- coding: utf-8 -*-
# author: Ethosa
from typing import Dict, Any


def create_button(
        button_type: str = "text",
        color: str = "primary",
        **kwargs
) -> Dict[str, Any]:
    """Creates a new Button object.

    :param button_type: button type.
    :param color: button color. Can be "primary", "secondary", "positive" or "negative".
    """
    obj = {}
    if button_type == "text":
        obj["color"] = color
    obj["action"] = kwargs
    obj["action"]["type"] = button_type
    return obj
