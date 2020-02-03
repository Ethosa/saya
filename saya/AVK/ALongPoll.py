# -*- coding: utf-8 -*-
# author: Ethosa

from ..VK.Event import event


class ALongPoll:
    def __init__(self, vk):
        """Class for using longpoll in VK

        Arguments:
            vk {Vk} -- authed VK object
        """
        self.v = vk.v
        self._log = vk._log
        self.debug = vk.debug
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

    async def _get_server(self):
        """
        Returns server, ts and key.

        Returns:
            {str}, {str}, {str} -- server, ts and key

        Raises:
            ValueError -- Invalid authentication.
        """
        response = await self.session.get(self.method, params=self.data)
        response = await response.json()
        if "response" in response:
            response = response["response"]
        else:
            raise ValueError("Invalid authentication.")
        return response["server"], response["ts"], response["key"]

    async def listen(self, ev=False):
        """
        Starts listening.

        Keyword Argments:
            ev {bool} -- always return dict object.

        Yields:
            {dict} -- new event
        """
        # Get server info and check it.
        server, ts, key = await self._get_server()

        await self._log("INFO", "LongPoll launched")

        # Start listening.
        while 1:
            response = await self.session.get(self.for_server % (server, key, ts))
            response = await response.json()
            if "ts" not in response or "updates" not in response:
                server, ts, key = await self._get_server()
                response = await self.session.get(self.for_server % (server, key, ts))
                response = await response.json()
            ts = response["ts"]

            for update in response["updates"]:
                if update:
                    if ev:
                        yield event(update)
                    else:
                        yield update
