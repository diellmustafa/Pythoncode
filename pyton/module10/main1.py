class Student:
    def __init__(self, name, age):
        self.name = name
        self.age = age


    @property
    def name(self):
        return self.__name

    @name.setter
    def name(self, name):
        self.__name = name

    @property
    def age(self):
        return self.__age
    @age.setter
    def age(self, age):
        self.__age = age

s = Student("John", 36)
print("Name of Student:", s.name)
print("Age of student:", s.age)

s.name = "Jhon"
s.age = 21

print("Updated name of student:", s.name)
print("Updated age of student:", s.age)