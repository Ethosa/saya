# -*- coding: utf-8 -*-
# author: Ethosa
import logging

import requests

from ..StartThread import StartThread

from .LongPoll import LongPoll
from .VkAuthManager import VkAuthManager
from .Uploader import Uploader
from .VkScript import VkScript


class Vk(object):
    def __init__(self, token="", group_id="",
                 login="", password="", api="5.103",
                 debug=False):
        """auth in VK

        Keyword Arguments:
            token {str} -- access_token (default: {""})
            group_id {str} -- group id if you want to log in through the group (default: {""})
            login {str} -- login. used for authorization through the user (default: {""})
            password {str} -- password. used for authorization through the user (default: {""})
            api {str} -- api version (default: {"5.103"})
            debug {bool} -- debug log (default: {False})
        """
        self.session = requests.Session()
        self.is_lp = False
        if login and password:
            self.auth = VkAuthManager(self, login, password)
            self.auth.login()
            token = self.auth.get_token()
            self.is_lp = True

        self.v = api
        self.token = token
        self.method = ""
        self.events = {}
        self.group_id = group_id

        self.debug = 50
        if debug:
            if isinstance(debug, int):
                self.debug = debug
            else:
                self.debug = 10
        logging.basicConfig(level=self.debug)

        self.execute = lambda code: self.call_method("execute", {"code": code})
        self.uploader = Uploader(self)
        self.longpoll = LongPoll(self)
        self.pyexecute = lambda code: self.call_method(
            "execute", {"code": VkScript().translate(code)}
        )

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
        data["v"] = self.v
        data["access_token"] = self.token
        response = self.session.post(
                "https://api.vk.com/method/%s" % method, data=data
            ).json()
        if "error" in response:
            logging.error('Error [%s] in called method "%s": %s' % (
                    response["error"]["error_code"], method, response["error"]["error_msg"]
                )
            )
        else:
            logging.debug('Successfully called method "%s"' % (method))
        return response

    def start_listen(self):
        """starts receiving events from the server
        """
        if not self.longpoll.lend:
            self.longpoll.lend = lambda event: self.start_listen

        logging.info("On")
        logging.info("Started to listen ...")

        for event in self.longpoll.listen(True):
            if "type" in event:
                if "event_%s" % event["type"] in self.events:
                    self.events["event_%s" % event["type"]](event)
                elif event["type"] in dir(self):
                    self.__getattribute__(event["type"])(event)
            else:
                logging.warning('Unknown event passed: "%s"' % (event))

    def __getattr__(self, attr):
        """a convenient alternative for the call_method method

        Arguments:
            attr {str} -- method name
            e.g. messages.send, wall.post

        Returns:
            response after calling method
        """
        if attr.startswith("on_"):
            attr = attr[3:]

            def decorator(func):
                obj_type = "%s" % type(func)

                def listen(f):
                    for event in self.longpoll.listen(True, True):
                        if event["type"] == attr:
                            func(event)
                if "method" in obj_type or "function" in obj_type:
                    StartThread(listen, func).start()
                else:
                    if func:
                        def _decorator(call):
                            StartThread(listen, call).start()
                        return _decorator
                    else:
                        def _decorator(call):
                            self.events["event_%s" % attr] = call
                            return call
                        return _decorator

            return decorator
        elif self.method:
            method = "%s.%s" % (self.method, attr)
            self.method = ""
            return lambda **data: self.call_method(method, data)
        else:
            self.method = attr
            return self
