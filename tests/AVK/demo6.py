# -*- coding: utf-8 -*-
# author: Ethosa
# Receiving real-time events #5

import asyncio
from random import randint

from saya import AVk


class MyAVk(AVk):
    async def message_new(self, event):
        print(event)
        if (event["text"] == "hello" and
                int(event["object"]["from"]) > 0):
            user = await vk.users.get(user_ids=event["object"]["from"])
            await vk.messages.send(
                message="Hello, %s!" % (user["response"][0]["first_name"]),
                random_id=randint(0, 100000),
                peer_id=event["peer_id"]
            )


async def main():
    await vk.start_listen()


vk = MyAVk(login=88005553535, password="qwerty", debug=True)
loop = asyncio.get_event_loop()
loop.run_until_complete(main())
