# Key OOP Principles (Encapsulation, Inheritance, Polymorphism, Abstraction)

# Inheritence

# class SuperClass:
#
#     class SubClass(Superclass):
#

class Animal:
    def sound(self):
        print("Some generic animal sound")
# class Dog(Animal):
#     def bark(self):
#         print("It barks")
#     def feed(self):
#         print("It feeds")

class Cat(Animal):
    def sound(self):
        print("Cat sound")
class Dog(Animal):
    def sound(self):
        print("Dog sound")

animal = Animal()
animal.sound()

cat = Cat()
cat.sound()
dog = Dog()
dog.sound()