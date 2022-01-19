# -*- coding: utf-8 -*-
# author: Ethosa
from typing import NoReturn, Optional, List, Dict, Any

class TemplateElement(dict):
    def __init__(
            self,
            title: str = "",
            description: str = "",
            photo_id: str = "",
            buttons: Optional[List[Dict[str, Any]]] = None,
            action: str = "open_link",
            link: str = "https://vk.com"
    ):
        """Initializes a new TemplateElement object.

        Keyword Arguments:
            :param title: template element title
            :param description: template element description
            :param photo_id:  Id of the picture, which must attach in the template element.
            :param buttons:  Buttons in TemplateElement.
            :param action:  Action of TemplateElement, can be "open_link" or "open_photo".
            :param link:  link for "open_link" action.
        """
        self["title"] = title
        self["description"] = description
        self["photo_id"] = photo_id
        self["buttons"] = buttons or []
        self["action"] = {"type": action}
        if action == "open_link":
            self["action"]["link"] = link

    def add(self, button) -> NoReturn:
        """Adds a new Button in TemplateElement.
        """
        if len(self["buttons"]) < 3:
            self["buttons"].append(button)
