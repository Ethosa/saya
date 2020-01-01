# -*- coding: utf-8 -*-
# author: Ethosa

from .Event import Event


class LongPoll:
    def __init__(self, vk):
        """Class for using longpoll in VK

        Arguments:
            vk {Vk} -- authed VK object
        """
        self.session = vk.session
        self.token = vk.token
        self.group_id = vk.group_id
        self.v = vk.v

        self.events = []
        self.opened = 0

        if self.group_id:
            self.method = "https://api.vk.com/method/groups.getLongPollServer"
            self.for_server = "%s?act=a_check&key=%s&ts=%s&wait=25"
        else:
            self.method = "https://api.vk.com/method/messages.getLongPollServer"
            self.for_server = "https://%s?act=a_check&key=%s&ts=%s&wait=25&mode=202&version=3"

    def listen(self, event=False):
        """Start listening

        Yields:
            {dict} -- new event
        """
        self.opened += 1
        data = {
            "access_token": self.token,
            "group_id": self.group_id,
            "v": self.v
        }
        if not self.group_id:
            del data["group_id"]
        response = self.session.get(self.method, params=data).json()["response"]

        server, ts, key = response["server"], response["ts"], response["key"]

        while 1:
            response = self.session.get(self.for_server % (server, key, ts)).json()
            ts = response["ts"]
            updates = response["updates"]

            for update in updates:
                if update:
                    if event:
                        yield Event(update)
                    else:
                        yield update

            if self.events:
                yield self.events.pop()

    def push(self, event):
        for _ in range(self.opened):
            self.events.append(event)
