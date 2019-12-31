from saya import Vk

vk = Vk(token="")
print(vk.call_method("messages.send", {"peer_id": 2_000_000_035, "message": "hello saya", "random_id": 123}))
