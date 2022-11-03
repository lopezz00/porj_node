import cua

s = cua.Stack()
print(s.isEmpty())
e1 = {
    "missatge": "Hola",
    "prioritat": 3
}
#s.push(e1)
print(s.isEmpty())


e2 = {
    "missatge": "Bona tarda",
    "prioritat": 2
}

e3 = {
    "missatge": "Adeu",
    "prioritat": 1
}

e4 = {
    "missatge": "e4",
    "prioritat": 3
}

"""
s.push(e1)
s.push(e2)
s.push(e2)
s.push(e4)
s.push(e2)
s.push(e3)
s.push(e3)
s.push(e1)
"""

s.push(e3)

for i in range(len(s)):
    print (s[i])


print("==============")
for i in range(len(s)):
    print(s.pop())