# -*- coding: utf-8 -*-
# author: Ethosa
from json import loads
from typing import Optional

from aiohttp.client_exceptions import WSServerHandshakeError

STREAMING_API_HEADERS = {
    "Content-Type": "application/json",
    "Connection": "upgrade",
    "Upgrade": "websocket",
    "Sec-Websocket-Version": "13"
}


class AStreamingAPI:
    def __init__(self, vk):
        """Initialize StreamingAPI object.

        Arguments:
            vk {Vk} -- Vk object.
        """
        self.logger = vk.logger
        self.session = vk.session
        self.call_method = vk.call_method

        self.url = ""

        self.endpoint: Optional[str] = None
        self.key: Optional[str] = None

    async def add_rule(self, tag, value):
        """Adds a new rule in the stream.

        Use this method to add a new rule to the stream.

        Arguments:
            tag {str} -- rule label.
            value {str} -- string representation of the rule.
        """
        obj = {
            "rule": {
                "value": value,
                "tag": tag
            }
        }
        response = await self.session.post(
            self.url,
            json=obj,
            headers={"Content-Type": "application/json"}
        )
        return await response.json()

    async def auth(self):
        """Logging into the Streaming API.

        Raises:
            ValueError -- wrong access token.

        Returns:
            dict -- result code.
        """
        response = await self.call_method("streaming.getServerUrl")
        if "response" in response:
            self.url = "https://%s/rules?key=%s" % (
                response["response"]["endpoint"],
                response["response"]["key"]
            )
            self.endpoint = response["response"]["endpoint"]
            self.key = response["response"]["key"]
        else:
            raise ValueError("%s" % response)

    async def delete_rule(self, tag):
        """Removes the rule from the stream.

        Use this method to remove a rule from a stream.

        Arguments:
            tag {str} -- rule label.

        Returns:
            dict -- result code.
        """
        response = await self.session.delete(
            self.url,
            json={"tag": tag},
            headers={"Content-Type": "application/json"}
        )
        return await response.json()

    async def get_rules(self):
        """Gets the current rules from the stream.

        Use this method to get rules that are already added to the stream.

        Returns:
            dict -- rules.
        """
        response = await self.session.get(self.url)
        return await response.json()

    async def listen(self):
        """Starts websocket listen

        Yields:
            dict -- event
        """
        if self.endpoint is None or self.key is None:
            await self.auth()
        url = "wss://%s/stream?key=%s" % (self.endpoint, self.key)
        while True:
            try:
                response = await self.session.ws_connect(
                    url, headers=STREAMING_API_HEADERS
                )
            except WSServerHandshakeError:
                continue
            data = await response.receive()
            yield loads(data.data)
            await response.close()
