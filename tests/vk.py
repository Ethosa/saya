from saya import Vk

# User
vk = Vk(login=81234567890, password="helloworld1", debug=True)

# Group
group = Vk(token="asdqwe1329balsduyhi_jbasuf", debug=True)


@vk.on_message_new(False)
def get_message(message):
    print(message)

vk.start_listen()
