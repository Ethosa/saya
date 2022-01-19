# -*- coding: utf-8 -*-
# author: Ethosa
from typing import Optional, NoReturn, Dict, Any, Generator
from json import loads

try:
    from websocket import create_connection
except ImportError:
    pass

STREAMING_API_HEADERS = {
    "Content-Type": "application/json",
    "Connection": "upgrade",
    "Upgrade": "websocket",
    "Sec-Websocket-Version": "13"
}


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

        self.endpoint: Optional[str] = None
        self.key: Optional[str] = None

    def add_rule(
            self,
            tag: str,
            value: str
    ) -> NoReturn:
        """Adds a new rule in the stream.

        Use this method to add a new rule to the stream.

        :param tag: rule label.
        :param value: string representation of the rule.
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

    def auth(self) -> NoReturn:
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

    def delete_rule(
            self,
            tag: str
    ) -> NoReturn:
        """Removes the rule from the stream.

        Use this method to remove a rule from a stream.

        :param tag: rule label.
        """
        return self.session.delete(
            self.url,
            json={"tag": tag},
            headers={"Content-Type": "application/json"}
        ).json()

    def get_rules(self) -> Dict[str, Any]:
        """Gets the current rules from the stream.

        Use this method to get rules that are already added to the stream.
        """
        return self.session.get(self.url, timeout=30).json()

    def listen(self) -> Generator[Dict[str, Any], None, None]:
        """Starts websocket listen
        """
        if self.endpoint is None or self.key is None:
            self.auth()
        while True:
            ws = create_connection(
                "wss://%s/stream?key=%s" % (
                    self.endpoint, self.key
                ),
                header=STREAMING_API_HEADERS
            )
            result = ws.recv()
            ws.close()
            yield loads(result)
