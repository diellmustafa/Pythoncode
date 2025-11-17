from os import write

file_path = "example.txt"

#reading file method
# file = open(file_path, "r")
#
# content = file.read()
# print(content)


#other reading file method
# with open(file_path, "r") as file:
#     content = file.read()
#     print(content)

# "r" read only mode
# "w" write
# "a" apennd
# "b" binary mode
# "x" exclusive creation

#reading lines
# with open("example.txt", "r") as file:
#     line1 = file.readlines()
#     print(line1)

#write in file
# with open(file_path, "w") as file:
#     file.write("Hi bro")
#
#write lines in file
# lines = ['Hello world\n', 'Welcome to Python\n']
# with open(file_path, "w") as file:
#     file.writelines(lines)

#append file
# with open(file_path, "a") as file:
#     file.write("New data appended")

# write binary data
# data = b"This is some binary data"
# with open("example.bin", "wb") as file:
#     file.write(data)

#read binary data
# with open("example.bin", "rb") as f:
#     data = f.read()
#     print(data) (?)

#print in clean lines
# with open(file_path) as cl:
#     for line in cl:
#         clean_line = line.strip()
#         print(clean_line)

#print in words
# with open("example.txt") as w:
#     for line in w:
#         words = line.strip().split()
#         print(words)

#write vars
# name = "Diell"
# age = 13
#
# with open('example.txt', 'w') as file:
#     file.write("Name "+ name + "\nAge " + str(age))

