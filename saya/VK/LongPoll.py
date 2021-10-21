# -*- coding: utf-8 -*-
# author: Ethosa
from time import sleep

from requests.exceptions import ConnectionError as RequestsConnectionError

from .Event import event


class LongPoll:
    def __init__(self, vk):
        """Class for using longpoll in VK

        Arguments:
            vk {Vk} -- authed VK object
        """
        self.v = vk.v
        self.logger = vk.logger
        self.session = vk.session
        self.ts = None
        self.server = None
        self.key = None

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
            self.for_server = (
                "https://%s?act=a_check&key=%s&ts=%s&wait=25&mode=202&version=3"
            )

    def _get_server(self):
        """
        Returns server, ts and key.

        Returns:
            {str}, {str}, {str} -- server, ts and key

        Raises:
            ValueError -- Invalid authentication.
        """
        while True:
            try:
                response = (
                    self.session.get(self.method, params=self.data).json()
                )
                break
            except RequestsConnectionError:
                self.logger.info(
                    "RequestsConnectionError happened, trying one more time"
                )
                sleep(.2)
        if "response" in response:
            response = response["response"]
        else:
            self.logger.error(response)
            raise ValueError("Invalid authentication.")
        self.server = response["server"]
        self.ts = response["ts"]
        self.key = response["key"]

    def _get_events(self):
        """
        Gets server events.

        Returns:
            dict -- server response.
        """
        while True:
            try:
                response = self.session.get(
                    self.for_server % (self.server, self.key, self.ts)
                ).json()
                if "ts" not in response or "updates" not in response:
                    self._get_server()
                else:
                    return response
            except RequestsConnectionError:
                self.logger.info(
                    "RequestsConnectionError happened, trying one more time"
                )
                sleep(.2)

    def listen(self, ev=False):
        """
        Starts listening.

        Keyword Argments:
            ev {bool} -- always return dict object.

        Yields:
            {dict} -- new event
        """
        # Get server info and check it.
        self._get_server()

        self.logger.info("LongPoll launched")

        # Start listening.
        while True:
            response = self._get_events()
            self.ts = response["ts"]

            for update in response["updates"]:
                if update:
                    if ev:
                        yield event(update)
                    else:
                        yield update
