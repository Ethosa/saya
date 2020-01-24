# -*- coding: utf-8 -*-
# author: Ethosa
import logging
from inspect import getsource

import regex
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

        # Parses vk.com, if login and password are not empty.
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

        # Debug settings.
        self.debug = 50
        if debug:
            if isinstance(debug, int):
                self.debug = debug
            else:
                self.debug = 10

        # Logger initialize.
        self.logger = logging.getLogger("saya")
        self.logger.setLevel(self.debug)
        handler = logging.StreamHandler()
        handler.setFormatter(
            logging.Formatter("[%(levelname)s] %(name)s: %(asctime)s — %(message)s")
        )
        self.logger.addHandler(handler)

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

        # Logging.
        if "error" in response:
            self.logger.error('Error [%s] in called method "%s": %s' % (
                    response["error"]["error_code"], method, response["error"]["error_msg"]
                )
            )
        else:
            self.logger.debug('Successfully called method "%s"' % (method))
        return response

    def to_execute(self, func):
        source = getsource(func)
        obj = regex.findall(r"\A@([^\.]+)", source)[0]
        args = regex.findall(
            r"\A[\S\s]+?def[ ]*[\S ]+?\(([^\)]*)\):",
            source
        )
        if args:
            args = regex.split(r"\s*,\s*", args[0])

        source = regex.sub(r"\A[\S\s]+?:\n[ ]+", r"", source)
        source = regex.sub("%s" % obj, "API", source)
        source = "\n\n%s\n\n" % (getsource(func))

        def execute(*arguments):
            code = source
            for arg, argument in zip(args, arguments):
                code = regex.sub(
                    r"([\r\n]+[^\"]+)\b" + arg + r"\b",
                    r"\1" + repr(argument),
                    code)
            if self.debug != 50:
                self.logger.debug(VkScript().translate(code))
            return self.pyexecute(code)
        return execute

    def start_listen(self):
        """starts receiving events from the server
        """
        self.logger.info("On")
        self.logger.info("Started to listen ...")

        for event in self.longpoll.listen(True):
            if "type" in event:
                if "event_%s" % event["type"] in self.events:
                    self.events["event_%s" % event["type"]](event)
                elif event["type"] in dir(self):
                    self.__getattribute__(event["type"])(event)
            else:
                self.logger.warning('Unknown event passed: "%s"' % (event))

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
                    for event in self.longpoll.listen(True):
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
