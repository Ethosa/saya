# -*- coding: utf-8 -*-
# author: Ethosa
# translate Python to VKScript
import asyncio

from saya import VkScript


async def main():
    vks = VkScript(use_regex=True)
    print(await vks.atranslate(script))

if __name__ == '__main__':
    script = """# This is comment.
a = "string variable"
b = 123
for i in range(10):
    b += 1
return b
"""
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
