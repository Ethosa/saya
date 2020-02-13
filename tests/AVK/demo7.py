# -*- coding: utf-8 -*-
# author: Ethosa
# upload photo in message and sending.
import asyncio

from saya import AVk, AUploader

vk = AVk(login=88005553535, password="qwerty", debug=True)


@vk.on_message_new
async def get_new_message(event):
    if event["text"] == "logo":
        # Upload photo
        response = await vk.uploader.message_photo(
            "logo2.png", peer_id=event["peer_id"]
        )
        # format response to "photo<OWNER_ID>_<ID>", e.g.: "photo213_123"
        photos = AUploader.format(response, "photo")
        # Send message
        await vk.messages.send(
            message="Library logo:",
            peer_id=event["peer_id"],
            attachment=photos
        )


async def main():
    await vk.start_listen()


if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
