# -*- coding: utf-8 -*-
# author: Ethosa

import requests

from .LongPoll import LongPoll
from .VkAuthManager import VkAuthManager


class Vk:
    def __init__(self, token="", group_id="",
                 login="", password="", api="5.103"):
        """auth in VK

        use it for auth in VK

        Keyword Arguments:
            token {str} -- access_token (default: {""})
            group_id {str} -- group id if you want to log in through the group (default: {""})
            login {str} -- login. used for authorization through the user (default: {""})
            password {str} -- password. used for authorization through the user (default: {""})
            api {str} -- api version (default: {"5.103"})
        """
        self.session = requests.Session()
        if login and password:
            auth = VkAuthManager(self, login, password)
            auth.login()
            token = auth.get_token()
        self.token = token
        self.group_id = group_id
        self.v = api
        self.method = ""
        self.longpoll = LongPoll(self)

    def call_method(self, method, data={}):
        """call to any method in VK api

        Arguments:
            method {str} -- method name
            e.g. "messages.send", "wall.post"

        Keyword Arguments:
            data {dict} -- data to send (default: {{}})

        Returns:
            {dict} -- response after calling method
        """
        data["access_token"] = self.token
        data["v"] = self.v
        response = self.session.post(
                "https://api.vk.com/method/%s" % method, data=data
            ).json()
        return response

    def __getattr__(self, attr):
        """a convenient alternative for the call_method method

        Arguments:
            attr {str} -- method name
            e.g. messages.send, wall.post

        Returns:
            response after calling method
        """
        if self.method:
            method = "%s.%s" % (self.method, attr)
            self.method = ""
            return lambda **data: self.call_method(method, data)
        else:
            self.method = attr
            return self
