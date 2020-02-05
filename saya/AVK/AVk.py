# -*- coding: utf-8 -*-
# author: Ethosa
from time import ctime as current_time

from aiohttp import ClientSession

from .ALongPoll import ALongPoll
from .AUploader import AUploader
from ..VK.VkAuthManager import VkAuthManager
from ..VK.VkScript import VkScript


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
        self.debug = debug

        self.method = ""
        self.events = {}

        self.longpoll = ALongPoll(self)
        self.uploader = AUploader(self)
        self.vks = VkScript()  # for pyexecute method.

    async def _log(self, logtype, message):
        """
        Outputs log messages.
        """
        if self.debug:
            print("[%s] at %s -- %s" % (
                logtype, current_time(), message)
            )

    async def _wrapper(self, **kwargs):
        """
        Provides convenient usage VK API.
        """
        return await self.call_method(self.method, kwargs)

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
        self.method = ""
        data["v"] = self.v
        data["access_token"] = self.token
        response = await self.session.post(
                "https://api.vk.com/method/%s" % method, data=data
            )
        response = await response.json()

        # Logging.
        if "error" in response:
            await self._log("ERROR", 'Error [%s] in called method "%s": %s' % (
                    response["error"]["error_code"], method,
                    response["error"]["error_msg"]
                )
            )
        else:
            await self._log("DEBUG", 'Successfully called method "%s"' % (method))
        return response

    async def execute(self, code):
        """
        Calls an execute VK API method

        Arguments:
            code {str} -- VKScript code.

        Returns:
            dict -- response
        """
        return await self.call_method("execute", {"code": code})

    async def pyexecute(self, code):
        """
        Calls an execute VK API method

        Arguments:
            code {str} -- Python code.

        Returns:
            dict -- response
        """
        code = await self.vks.atranslate(code)
        return await self.execute(code)

    async def start_listen(self):
        """
        Starts receiving events from the server.
        """
        async for event in self.longpoll.listen(True):
            if "type" in event:
                if event["type"] in self.events:
                    await self.events[event["type"]](event)
                elif event["type"] in dir(self):
                    await getattr(self, event["type"])(event)
            else:
                self._log("WARNING", "Unknown event passed: %s" % (event))

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
            self.method = "%s.%s" % (self.method, attr)
            return self._wrapper
        else:
            self.method = attr
            return self
