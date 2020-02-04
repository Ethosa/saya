# -*- coding: utf-8 -*-
# author: Ethosa
# upload photo in message and sending.
from saya import Vk, Uploader

vk = Vk(login=88005553535, password="qwerty", debug=True)


@vk.on_message_new(False)
def get_new_message(event):
    if event["text"] == "logo":
        # Upload photo
        response = vk.uploader.message_photo(
            "logo.png", peer_id=event["peer_id"]
        )
        # format response to "photo<OWNER_ID>_<ID>", e.g.: "photo213_123"
        photos = Uploader.format(response, "photo")
        # Send message
        vk.messages.send(
            message="Library logo:",
            peer_id=event["peer_id"],
            attachment=photos
        )

if __name__ == '__main__':
    vk.start_listen()
