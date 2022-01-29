# -*- coding: utf-8 -*-
# author: Ethosa
from typing import NoReturn, Dict, Any, Optional
from asyncio import sleep, TimeoutError

from aiohttp.client_exceptions import ClientConnectionError

from ..VK.event import event


class ALongPoll:
    def __init__(self, vk):
        """Class for using longpoll in VK

        Arguments:
            vk {Vk} -- authed VK object
        """
        self.v = vk.v
        # noinspection PyProtectedMember
        self._log = vk._log
        self.debug = vk.debug
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

    async def _get_server(self) -> NoReturn:
        """Returns server, ts and key.

        Raises:
            ValueError -- Invalid authentication.
        """
        response = await (
            await self.session.get(self.method, params=self.data)
        ).json()
        if "response" in response:
            response = response["response"]
        else:
            raise ValueError("Invalid authentication.")
        self.server = response["server"]
        self.ts = response["ts"]
        self.key = response["key"]

    async def _get_events(self) -> Optional[Dict[str, Any]]:
        """Returns server response after calling.
        """
        try:
            response = await self.session.get(
                self.for_server % (self.server, self.key, self.ts)
            )
            response = await response.json()
            if "ts" not in response or "updates" not in response:
                await self._get_server()
            else:
                return response
        except ClientConnectionError:
            self._log('WARNING', 'connection error... trying restart listening in 5 seconds...')
            await sleep(5)
            return None
        except TimeoutError:
            self._log('WARNING', 'timeout error... trying restart listening in 10 seconds...')
            await sleep(10)
            return None
        except Exception as e:
            self._log('WARNING', 'Unknown exception... trying restart listening in 15 seconds...')
            self._log('ERROR', e)
            await sleep(15)
            return None

    async def listen(
            self,
            ev: bool = False
    ):
        """Starts listening.

        Keyword Argments:
            ev {bool} -- always return dict object.

        Yields:
            {dict} -- new event
        """
        # Get server info and check it.
        await self._get_server()

        self._log("INFO", "LongPoll launched")

        # Start listening.
        while True:
            response = await self._get_events()
            if not response:
                continue
            self.ts = response["ts"]

            for update in response["updates"]:
                if update:
                    if ev:
                        yield event(update)
                    else:
                        yield update
