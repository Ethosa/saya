from saya import Vk

vk = Vk(login=123, password="123", debug=True)


@vk.to_execute
def hello(a, b, c, arg1):
    test = a
    test = test + b
    test = test + c
    test = test + "a"
    vk.messages.send(
        message=test,
        peer_id=2_000_000_035,
        random_id=4,
    )
    vk.messages.send(message=test,
                     peer_id=2_000_000_035,
                     random_id=5)
    return test

print(hello("бан блин))) ", "а блин :| ",
            "bbbbbbbbbb", 13123123123))
