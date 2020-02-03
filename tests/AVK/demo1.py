# -*- coding: utf-8 -*-
# author: Ethosa
# Message sending.

import asyncio

from saya import AVk

vk = AVk(login=88005553535, password="qwerty", debug=True)


async def main():
    await vk.messages.send(message="Hello, Saya!",
                           peer_id=123123,
                           random_id=123)

loop = asyncio.get_event_loop()
loop.run_until_complete(main())
