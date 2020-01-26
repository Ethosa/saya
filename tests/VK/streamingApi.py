from saya import Vk, StreamingAPI

vk = Vk(token="service token here :3", debug=True)

streaming = StreamingAPI(vk)
streaming.auth()
streaming.add_rule("1", "аниме")
streaming.add_rule("2", "saya")
streaming.add_rule("3", "кот")
print(streaming.get_rules())

for event in streaming.listen():
    print(event)
