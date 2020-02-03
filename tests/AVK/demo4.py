# -*- coding: utf-8 -*-
# author: Ethosa
# Receiving real-time events #3

import asyncio

from saya import AVk


class MyAVk(AVk):
    async def message_new(self, event):
        print(event)


async def main():
    await vk.start_listen()


vk = MyAVk(login=88005553535, password="qwerty", debug=True)
loop = asyncio.get_event_loop()
loop.run_until_complete(main())
