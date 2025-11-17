# name = ["Rubik", "Rion", "Yll", "Diell"]
#
# for name in name:
#     print(name)
#
# test1 = ("hello")

# for test1 in test1:
#     print(test1)
#
# test2 = "hello world"
# for character in test2:
#     if character.isalpha():
#         print(character)

# for number in range(1, 6):
#     print(number)

# numbers = [12, 32, 33, 34, 25]
#
# maximum = numbers[0]
#
# for num in numbers:
#         num > maximum
#         maximum = num
#         print("The max value is", maximum)

# count = 1
#
# while count < 5:
#     print(count)
#     count += 1

# numbers = [1, 2, 3, 4, 5]
# target = 4
#
# for number in numbers:
#     print(number)
#     if number == target:
#         print("Target found")
#         break

# scores = [50, 42, 68, 35, 73, 29, 81, 63]
# total = 0
# count = 0
#
# for score in scores:
#     if score < 50:
#         continue
#
#     total += score
#     count += 1
#
#     average = total / count if count > 0 else 0
#     print("Average score above 50 is", average)

# while True:
#     user_input = print("Enter a positive number: ")
#     if user_input.isnumeric():
#         number = int(user_input)
#         if number > 0:
#             break
#         print("Error")
#print("You printed a positive number")

# total = 0
#
# for number in range(1, 11):
#     if number % 2 == 0:
#         total += number
# print(total)
