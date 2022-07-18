read = str("192.168.150.5")

splited = read.split('.')

print(splited)
splited.pop()
print(splited)
splited.append("1/24")
read = ".".join(splited)
print(read)