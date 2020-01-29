# -*- coding: utf-8 -*-
# author: Ethosa

from .Event import event
from ..Deprecated import deprecated


class LongPoll:
    def __init__(self, vk):
        """Class for using longpoll in VK

        Arguments:
            vk {Vk} -- authed VK object
        """
        self.v = vk.v
        self.logger = vk.logger
        self.session = vk.session

        self.data = {
            "access_token": vk.token,
            "v": vk.v
        }

        if vk.group_id:
            self.data["group_id"] = vk.group_id
            self.method = "https://api.vk.com/method/groups.getLongPollServer"
            self.for_server = "%s?act=a_check&key=%s&ts=%s&wait=25"
        else:
            self.method = "https://api.vk.com/method/messages.getLongPollServer"
            self.for_server = "https://%s?act=a_check&key=%s&ts=%s&wait=25&mode=202&version=3"

    def _get_server(self):
        """
        Returns server, ts and key.

        Returns:
            {str}, {str}, {str} -- server, ts and key

        Raises:
            ValueError -- Invalid authentication.
        """
        response = self.session.get(self.method, params=self.data).json()
        if "response" in response:
            response = response["response"]
        else:
            raise ValueError("Invalid authentication.")
        server, ts, key = response["server"], response["ts"], response["key"]
        return server, ts, key

    def listen(self, ev=False):
        """
        Starts listening.

        Keyword Argments:
            ev {bool} -- always return dict object.

        Yields:
            {dict} -- new event
        """
        # Get server info and check it.
        server, ts, key = self._get_server()

        self.logger.info("LongPoll launched")

        # Start listening.
        while 1:
            response = self.session.get(self.for_server % (server, key, ts)).json()
            if "ts" not in response or "updates" not in response:
                server, ts, key = self._get_server()
                response = self.session.get(self.for_server % (server, key, ts)).json()
            ts = response["ts"]
            updates = response["updates"]

            for update in updates:
                if update:
                    if ev:
                        yield event(update)
                    else:
                        yield update

    @deprecated("0.1.52", "0.2.0")
    def on_listen_end(self, call):
        pass

    @deprecated("0.1.52", "0.2.0")
    def push(self, ev):
        pass
