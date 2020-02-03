# -*- coding: utf-8 -*-
# author: Ethosa
from logging import getLogger, StreamHandler, Formatter

from aiohttp import ClientSession

from .ALongPoll import ALongPoll
from ..VK.VkAuthManager import VkAuthManager


class AVk:
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
        self.session = ClientSession()

        # Parses vk.com, if login and password are not empty.
        if login and password:
            self.auth = VkAuthManager()
            self.auth.login(login, password)
            token = self.auth.get_token()

        self.v = api
        self.token = token
        self.group_id = group_id

        self.method = ""
        self.current_method = ""
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

        self.longpoll = ALongPoll(self)

    async def _wrapper(self, **kwargs):
        """
        Provides convenient usage VK API.
        """
        return await self.call_method(self.current_method, kwargs)

    async def call_method(self, method, data={}):
        """
        Calls to any method in VK API.

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
        response = await self.session.post(
                "https://api.vk.com/method/%s" % method, data=data
            )
        response = await response.json()

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

    async def start_listen(self):
        """
        Starts receiving events from the server.
        """
        async for event in self.longpoll.listen(True):
            if event["type"] in self.events:
                await self.events[event["type"]](event)
            elif event["type"] in dir(self):
                await getattr(self, event["type"])(event)

    def __getattr__(self, attr):
        """
        A convenient alternative for the call_method method.

        Arguments:
            attr {str} -- method name
            e.g. messages.send, wall.post

        Returns:
            response after calling method
        """
        if attr.startswith("on_"):
            attr = attr[3:]

            def _decorator(call):
                self.events[attr] = call
                return call
            return _decorator
        elif self.method:
            method = "%s.%s" % (self.method, attr)
            self.method = ""
            self.current_method = method
            return self._wrapper
        else:
            self.method = attr
            return self
