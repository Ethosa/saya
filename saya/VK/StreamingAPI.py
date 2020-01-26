# -*- coding: utf-8 -*-
# author: Ethosa
from json import loads

from websocket import create_connection


class StreamingAPI:
    def __init__(self, vk):
        """Initialize StreamingAPI object.

        Arguments:
            vk {Vk} -- Vk object.
        """
        self.logger = vk.logger
        self.session = vk.session
        self.call_method = vk.call_method

        self.url = ""

    def add_rule(self, tag, value):
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
        return self.session.post(
            self.url,
            json=obj,
            headers={"Content-Type": "application/json"}
        ).json()

    def auth(self):
        """Logging into the Streaming API.

        Raises:
            ValueError -- wrong access token.

        Returns:
            dict -- result code.
        """
        response = self.call_method("streaming.getServerUrl")
        if "response" in response:
            self.url = "https://%s/rules?key=%s" % (
                response["response"]["endpoint"],
                response["response"]["key"]
            )
            self.endpoint = response["response"]["endpoint"]
            self.key = response["response"]["key"]
        else:
            raise ValueError("%s" % response)

    def delete_rule(self, tag):
        """Removes the rule from the stream.

        Use this method to remove a rule from a stream.

        Arguments:
            tag {str} -- rule label.

        Returns:
            dict -- result code.
        """
        return self.session.delete(
            self.url,
            json={"tag": tag},
            headers={"Content-Type": "application/json"}
        ).json()

    def get_rules(self):
        """Gets the current rules from the stream.

        Use this method to get rules that are already added to the stream.

        Returns:
            dict -- rules.
        """
        return self.session.get(self.url).json()

    def listen(self):
        """Starts websocket listen

        Yields:
            dict -- event
        """
        while 1:
            ws = create_connection(
                "wss://%s/stream?key=%s" % (
                    self.endpoint, self.key
                ),
                header=[
                    "Content-Type: application/json",
                    "Connection: upgrade",
                    "Upgrade: websocket",
                    "Sec-Websocket-Version: 1",
                ]
            )
            result = ws.recv()
            ws.close()
            yield loads(result)
