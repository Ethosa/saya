# -*- coding: utf-8 -*-
# author: Ethosa


class TemplateElement(dict):
    def __init__(self, title="", description="",
                 photo_id="", buttons=[], action="open_link",
                 link="https://vk.com"):
        self["title"] = title
        self["description"] = description
        self["photo_id"] = photo_id
        self["buttons"] = buttons
        self["action"] = {"type": action}
        if action == "open_link":
            self["action"]["link"] = link

    def add(self, button):
        if len(self["buttons"]) < 3:
            self["buttons"].append(button)
