from saya.Deprecated import deprecated


@deprecated("0.1", "0.3")
def deprecated_test():
    print("not deprecated!")

deprecated_test()
