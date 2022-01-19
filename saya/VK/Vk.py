# -*- coding: utf-8 -*-
# author: Ethosa
from typing import Union, Optional, Dict, Any, NoReturn
from logging import getLogger, StreamHandler, Formatter

from requests import Session

from .longpoll import LongPoll
from .uploader import Uploader
from .vk_auth import VkAuthManager
from .vks import VkScript
from ..StartThread import StartThread


class Vk(object):
    def __init__(
            self,
            token: str = "",
            group_id: Union[str, int] = "",
            login: str = "",
            password: str = "",
            api: str = "5.103",
            debug: bool = False
    ):
        """auth in VK

        :param token: access_token
        :param group_id: group id if you want to log in through the group
        :param login: login. used for authorization through the user
        :param password: password. used for authorization through the user
        :param api: api version
        :param debug: debug log
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
        self.vks = VkScript()  # for pyexecute method.

    def call_method(
            self,
            method: str,
            data: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """call to any method in VK api

        :param method: method name e.g. "messages.send", "wall.post"
        :param data: data to send
        """
        if not data:
            data = {}
        data["v"] = self.v
        data["access_token"] = self.token
        response = self.session.post(
            "https://api.vk.com/method/%s" % method,
            data=data, timeout=30
        ).json()

        # Logging.
        if "error" in response:
            self.logger.error(
                'Error [%s] in called method "%s": %s' % (
                    response["error"]["error_code"], method,
                    response["error"]["error_msg"]
                )
            )
        else:
            self.logger.debug('Successfully called method "%s"' % method)
        return response

    def execute(
            self,
            code: str
    ) -> Dict[str, Any]:
        """Calls an execute VK API method

        :param code: VKScript code.
        """
        return self.call_method("execute", {"code": code})

    def pyexecute(
            self,
            code
    ) -> Dict[str, Any]:
        """Calls an execute VK API method

        :param code: Python code.
        """
        return self.execute(self.vks.translate(code))

    def start_listen(self) -> NoReturn:
        """Starts receiving events from the server.
        """
        for event in self.longpoll.listen(True):
            if "type" in event:
                if event["type"] in self.events:
                    self.events[event["type"]](event)
                elif event["type"] in dir(self):
                    getattr(self, event["type"])(event)
            else:
                self.logger.warning('Unknown event passed: "%s"' % event)

    def __getattr__(
            self,
            attr: str
    ) -> Any:
        """A convenient alternative for the call_method method.

        :param attr: method name e.g. messages.send, wall.post
        """
        if attr.startswith("on_"):  # e.g. on_message_new
            attr = attr[3:]

            def decorator(obj):
                def listen(_f):
                    for event in self.longpoll.listen(True):
                        if event["type"] == attr:
                            obj(event)

                if isinstance(obj, callable):
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
