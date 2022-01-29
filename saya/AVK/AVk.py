# -*- coding: utf-8 -*-
# author: Ethosa
from typing import NoReturn, Optional, Dict, Any
import asyncio
from time import ctime as current_time

from aiohttp import ClientSession

from .alongpoll import ALongPoll
from .auploader import AUploader
from ..VK.vk_auth import VkAuthManager
from ..VK.vks import VkScript


class AVk:
    def __init__(
            self,
            token: str = "",
            group_id: str = "",
            login: str = "",
            password: str = "",
            api: str = "5.103",
            debug: bool = False,
            loop: Optional[asyncio.EventLoop] = None
    ) -> NoReturn:
        """auth in VK

        :param token: access_token
        :param group_id: group id if you want to log in through the group
        :param login: login. used for authorization through the user
        :param password: password. used for authorization through the user
        :param api: api version
        :param debug: debug log
        :param loop: event loop to use for requests
        """
        self.session = ClientSession(loop=loop or asyncio.get_event_loop())

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

    def _log(
            self,
            logtype: str,
            message: str
    ) -> NoReturn:
        """Outputs log messages.
        """
        if self.debug:
            print("[%s] at %s -- %s" % (
                logtype, current_time(), message)
            )

    async def _wrapper(
            self,
            **kwargs
    ) -> Dict[str, Any]:
        """Provides convenient usage VK API.
        """
        return await self.call_method(self.method, kwargs)

    async def call_method(
            self,
            method,
            data: Dict[str, Any] = None
    ) -> Dict[str, Any]:
        """Calls to any method in VK API.

        Arguments:
            method {str} -- method name
            e.g. "messages.send", "wall.post"

        Keyword Arguments:
            data {dict} -- data to send (default: {{}})

        Returns:
            dict -- response after calling method
        """
        self.method = ""
        if not data:
            data = {}
        data["v"] = self.v
        data["access_token"] = self.token
        response = await self.session.post(
            "https://api.vk.com/method/%s" % method, data=data
        )
        response = await response.json()

        # Logging.
        if "error" in response:
            self._log("ERROR", 'Error [%s] in called method "%s": %s' % (
                    response["error"]["error_code"], method,
                    response["error"]["error_msg"]
                )
            )
        else:
            self._log("DEBUG", 'Successfully called method "%s"' % method)
        return response

    async def execute(
            self,
            code: str
    ) -> Dict[str, Any]:
        """Calls an execute VK API method

        Arguments:
            code {str} -- VKScript code.

        Returns:
            dict -- response
        """
        return await self.call_method("execute", {"code": code})

    async def pyexecute(
            self,
            code
    ) -> Dict[str, Any]:
        """Calls an execute VK API method

        Arguments:
            code {str} -- Python code.

        Returns:
            dict -- response
        """
        code = self.vks.atranslate(code)
        return await self.execute(code)

    async def start_listen(self):
        """Starts receiving events from the server.
        """
        async for event in self.longpoll.listen(True):
            if "type" in event:
                try:
                    handler = self.events[event["type"]]
                except KeyError:
                    handler = getattr(self, event["type"])
                if event['type'] in self.events or event['type'] in dir(self):
                    asyncio.create_task(handler(event))
            else:
                self._log("WARNING", "Unknown event passed: %s" % event)

    def __getattr__(self, attr):
        """A convenient alternative for the call_method method.

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
