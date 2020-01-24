# -*- coding: utf-8 -*-
# author: Ethosa

from .Event import Event
from ..Deprecated import deprecated


class LongPoll:
    def __init__(self, vk):
        """Class for using longpoll in VK

        Arguments:
            vk {Vk} -- authed VK object
        """
        self.v = vk.v
        self.logger = vk.logger
        self.token = vk.token
        self.session = vk.session
        self.group_id = vk.group_id

        if self.group_id:
            self.method = "https://api.vk.com/method/groups.getLongPollServer"
            self.for_server = "%s?act=a_check&key=%s&ts=%s&wait=25"
        else:
            self.method = "https://api.vk.com/method/messages.getLongPollServer"
            self.for_server = "https://%s?act=a_check&key=%s&ts=%s&wait=25&mode=202&version=3"

    def listen(self, event=False):
        """Starts listening.

        Yields:
            {dict} -- new event
        """
        data = {
            "access_token": self.token,
            "group_id": self.group_id,
            "v": self.v
        }
        if not self.group_id:
            del data["group_id"]

        # Get server info and check it.
        response = self.session.get(self.method, params=data).json()
        if "response" in response:
            response = response["response"]
        else:
            raise ValueError("Invalid authentication.")
        server, ts, key = response["server"], response["ts"], response["key"]

        self.logger.info("LongPoll launched")

        # Start listening.
        while 1:
            response = self.session.get(self.for_server % (server, key, ts)).json()
            if "ts" not in response or "updates" not in response:
                response = self.session.get(self.method, params=data).json()["response"]
                server, ts, key = response["server"], response["ts"], response["key"]
                response = self.session.get(self.for_server % (server, key, ts)).json()
            ts = response["ts"]
            updates = response["updates"]

            for update in updates:
                if update:
                    if event:
                        yield Event(update)
                    else:
                        yield update

    @deprecated("0.1.52")
    def on_listen_end(self, call):
        pass

    @deprecated("0.1.52")
    def push(self, event):
        pass
