# try:
#     result = 10 / 0
# except ZeroDivisionError:
#     print("You can't divide by zero")
#
#
# fruits = {
#     "apple": 10,
#     "banana": 20,
#     "orange": 30,
# }
#
# try:
#     print(fruits["cherry"])
# except KeyError:
#     print("You can't find the fruit cherry")

# text = "this is a text"
#
# try:
#     text_to_int = int(text)
# except Exception as e:
#     print("An error has occured:", e)

def divide_number(a, b):
    try:
        result = a / b
        print("Result is:", result)
    except ZeroDivisionError:
        print("You can't divide by zero")
    except TypeError:
        print("Invalid type of division")
    except Exception as e:
        print("An error will typecasting", e)

divide_number(10, 2)
divide_number(10, 0)
divide_number("Hi", 5)
