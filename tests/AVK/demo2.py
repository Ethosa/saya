# -*- coding: utf-8 -*-
# author: Ethosa
# Receiving real-time events #1

import asyncio

from saya import AVk

vk = AVk(login=88005553535, password="qwerty", debug=True)


async def main():
    async for event in vk.longpoll.listen(True):
        print(event)

loop = asyncio.get_event_loop()
loop.run_until_complete(main())
