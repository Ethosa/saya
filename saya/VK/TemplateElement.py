# -*- coding: utf-8 -*-
# author: Ethosa


class TemplateElement(dict):
    def __init__(self, title="", description="",
                 photo_id="", buttons=[], action="open_link",
                 link="https://vk.com"):
        """Initializes a new TemplateElement object.

        Keyword Arguments:
            title {str} (default: {""})
            description {str} (default: {""})
            photo_id {str} -- Id of the picture, which must attach in the template element. (default: {""})
            buttons {list} -- Buttons in TemplateElement. (default: {[]})
            action {str} -- Action of TemplateElement, can be "open_link" or "open_photo". (default: {"open_link"})
            link {str} -- link for "open_link" action. (default: {"https://vk.com"})
        """
        self["title"] = title
        self["description"] = description
        self["photo_id"] = photo_id
        self["buttons"] = buttons
        self["action"] = {"type": action}
        if action == "open_link":
            self["action"]["link"] = link

    def add(self, button):
        """Adds a new Button in TemplateElement.

        Arguments:
            button {Button} -- Button object.
        """
        if len(self["buttons"]) < 3:
            self["buttons"].append(button)
