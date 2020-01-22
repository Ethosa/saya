# -*- coding: utf-8 -*-
# author: Ethosa
import logging

from .Event import Event


class LongPoll:
    def __init__(self, vk):
        """Class for using longpoll in VK

        Arguments:
            vk {Vk} -- authed VK object
        """
        self.v = vk.v
        self.debug = vk.debug
        logging.basicConfig(level=self.debug)
        self.token = vk.token
        self.session = vk.session
        self.group_id = vk.group_id

        self.lend = lambda arg: None
        self.opened = 0
        self.events = []

        if self.group_id:
            self.method = "https://api.vk.com/method/groups.getLongPollServer"
            self.for_server = "%s?act=a_check&key=%s&ts=%s&wait=25"
        else:
            self.method = "https://api.vk.com/method/messages.getLongPollServer"
            self.for_server = "https://%s?act=a_check&key=%s&ts=%s&wait=25&mode=202&version=3"

    def listen(self, event=False, autorestart=False):
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

        logging.info("LongPoll launched")

        while 1:
            response = self.session.get(self.for_server % (server, key, ts)).json()
            if "ts" not in response or "updates" not in response:
                if not autorestart:
                    break
                else:
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

            if self.events:
                yield self.events.pop()
        if self.debug:
            logging.error("LongPoll has been stopped. Trying to restart ...")
        self.lend(event)

    def on_listen_end(self, call):
        """Sets the function that is called when listening is completed.

        Arguments:
            call {method, function or class} -- callable object

        Returns:
            call
        """
        self.lend = call
        return call

    def push(self, event):
        """Adds a new event to Longpoll

        Arguments:
            event {dict} -- event info. Must contain a "type" key for normal operation
        """
        for _ in range(self.opened):
            self.events.append(event)
