# def calculate_area(length, width):
#     return length * width
#
# def calculate_perimeter(length, width):
#     return 2 * (length + width)
#
#
#
# length = 5
# width = 3
#
#
# area = calculate_area(length, width)
# perimeter = calculate_perimeter(length, width)
#
# print(f"Area of area is {area}")
# print(f"Perimeter of area is {perimeter}")

# class Rectangle:
#     def __init__(self, length, width):
#         self.length = length
#         self.width = width
#
#     def calculate_area(self):
#         return self.length * self.width
#     def calculate_perimeter(self):
#         return self.length + self.width
#
# my_rectangle = Rectangle(10, 10)
#
# area = my_rectangle.calculate_area()
# perimeter = my_rectangle.calculate_perimeter()
#
# print(f"Area: {area}")
# print(f"Perimeter: {perimeter}")

# class Person:
#     def __init__(self, name, age):
#         self.name = name
#         self.age = age
#
#     def greet(self):
#         print(f"Hello {self.name}, you are {self.age} years old.")
#
# person1 = Person("John", 20)
# person2 = Person("Rubik", 15)
#
# person1.greet()
# person2.greet()

# class Student:
#     school_name = "Digital School"
#
# student1 = Student()
#
# print(student1.school_name)

# class Student:
#     school_name = "Digital School"
#
#     def __init__(self, name, age, course):
#         self.name = name
#         self.age = age
#         self.course = course
#
# studenti1 = Student("Diell", 17, "Python")
# studenti2 = Student("Brim", 63, "C++")
#
# print(studenti1.course)
# print(studenti2.course)

# class MyClass:
#     def __init__(self):
#         self.__private_variable = "This is a private variable"
#         # self.public_variable = "This is a public variable"
#     def __private_method(self):
#         print("This is a private method")

# my_class = MyClass()
# print(my_class.public_variable)

# my_class = MyClass()
# print(my_class.__private_variable)

# my_class.__private_method()

class MyClass:
    def __init__(self):
        self._protected_variable = "Hello World"

    def _protected_method(self):
        print("Protected Method")

my_class = MyClass()

print(my_class._protected_variable)

print(my_class._protected_method())