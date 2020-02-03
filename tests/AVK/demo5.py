# -*- coding: utf-8 -*-
# author: Ethosa
# Receiving real-time events #4

import asyncio
from random import randint

from saya import AVk


class MyAVk(AVk):
    async def message_new(self, event):
        print(event)
        if event["text"] == "hello":
            await vk.messages.send(
                message="Hello, Saya!",
                random_id=randint(0, 100000),
                peer_id=event["peer_id"]
            )


async def main():
    await vk.start_listen()


vk = MyAVk(login=88005553535, password="qwerty", debug=True)
loop = asyncio.get_event_loop()
loop.run_until_complete(main())
