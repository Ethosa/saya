from saya import VkScript

script = """
# hello world program
a = 15
b = 10
b = 5

array_test = [1, 2, 3, 4, 5, 6]
array_sliced = array_test[2:]
array_sliced = array_test[2:-1]
array_sliced = array_test[:-1]
array_sliced.insert(0, 1)
array_sliced.append(1)

for i in range(10):
    a += 5

if 1 == 2:
    a += 2
elif 1 == 1:
    a += 100
else:
    a += 5

return array_sliced
"""

script = VkScript().translate(script)
print(script)
