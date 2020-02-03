# -*- coding: utf-8 -*-
# author: Ethosa
from logging import getLogger, StreamHandler, Formatter
from inspect import getsource

from regex import findall, sub, split
from requests import Session

from .LongPoll import LongPoll
from .VkAuthManager import VkAuthManager
from .Uploader import Uploader
from .VkScript import VkScript

from ..StartThread import StartThread
from ..Deprecated import deprecated


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
        self.session = Session()

        # Parses vk.com, if login and password are not empty.
        if login and password:
            self.auth = VkAuthManager()
            self.auth.login(login, password)
            token = self.auth.get_token()

        self.v = api
        self.token = token
        self.group_id = group_id

        self.method = ""
        self.events = {}

        # Debug settings.
        self.debug = 50
        if debug:
            if isinstance(debug, int):
                self.debug = debug
            else:
                self.debug = 10

        # Logger initialize.
        self.logger = getLogger("saya")
        self.logger.setLevel(self.debug)
        handler = StreamHandler()
        handler.setFormatter(
            Formatter("[%(levelname)s] %(name)s: %(asctime)s — %(message)s")
        )
        self.logger.addHandler(handler)

        self.uploader = Uploader(self)
        self.longpoll = LongPoll(self)

    def call_method(self, method, data={}):
        """call to any method in VK api

        Arguments:
            method {str} -- method name
            e.g. "messages.send", "wall.post"

        Keyword Arguments:
            data {dict} -- data to send (default: {{}})

        Returns:
            dict -- response after calling method
        """
        data["v"] = self.v
        data["access_token"] = self.token
        response = self.session.post(
                "https://api.vk.com/method/%s" % method, data=data
            ).json()

        # Logging.
        if "error" in response:
            self.logger.error('Error [%s] in called method "%s": %s' % (
                    response["error"]["error_code"], method,
                    response["error"]["error_msg"]
                )
            )
        else:
            self.logger.debug('Successfully called method "%s"' % (method))
        return response

    def execute(self, code):
        """
        Calls an execute VK API method

        Arguments:
            code {str} -- VKScript code.

        Returns:
            dict -- response
        """
        return self.call_method("execute", {"code": code})

    def pyexecute(self, code):
        """
        Calls an execute VK API method

        Arguments:
            code {str} -- Python code.

        Returns:
            dict -- response
        """
        return self.execute(VkScript().translate(code))

    @deprecated("0.1.81", "0.2.0")
    def to_execute(self, func):
        """Converts function code to the VKScript code.

        When you call a function using the to_execute decorator, you call its VKScript version.

        Arguments:
            func {function} -- callable object.

        Returns:
            func
        """
        source = getsource(func)
        source_code = "\n\n%s\n\n" % (source)
        obj = findall(r"\A@([^\.]+)", source)[0]
        args = findall(
            r"\A[\S\s]+?def[ ]*[\S ]+?\(([^\)]*)\):",
            source
        )
        if args:
            args = split(r"\s*,\s*", args[0])

        source = sub(r"\A[\S\s]+?:\n[ ]+", r"", source)
        source = sub("%s" % obj, "API", source)

        def _execute(*arguments):
            code = source_code
            for arg, argument in zip(args, arguments):
                code = sub(
                    r"([\r\n]+[^\"]+)\b" + arg + r"\b",
                    r"\1" + repr(argument),
                    code)
            code = VkScript().translate(code)
            self.logger.debug(code)
            return self.execute(code)
        return _execute

    def start_listen(self):
        """
        Starts receiving events from the server.
        """
        for event in self.longpoll.listen(True):
            if "type" in event:
                if event["type"] in self.events:
                    self.events[event["type"]](event)
                elif event["type"] in dir(self):
                    getattr(self, event["type"])(event)
            else:
                self.logger.warning('Unknown event passed: "%s"' % (event))

    def __getattr__(self, attr):
        """A convenient alternative for the call_method method.

        Arguments:
            attr {str} -- method name
            e.g. messages.send, wall.post

        Returns:
            response after calling method
        """
        if attr.startswith("on_"):  # e.g. on_message_new
            attr = attr[3:]

            def decorator(obj):
                def listen(f):
                    for event in self.longpoll.listen(True):
                        if event["type"] == attr:
                            obj(event)

                if callable(obj):
                    StartThread(listen, obj).start()
                else:
                    # obj should be boolean
                    if obj:
                        def _decorator(call):
                            StartThread(listen, call).start()
                    else:
                        def _decorator(call):
                            self.events[attr] = call
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
