from abc import ABC, abstractmethod


# Abstract Base Class for Person
class Person(ABC):
    def __init__(self, name, age, weight, height):
        self.name = name
        self.age = age
        self._weight = weight
        self._height = height

    @property
    def weight(self):
        return self._weight

    @weight.setter
    def weight(self, value):
        if value <= 0:
            raise ValueError("Weight must be greater than zero.")
        self._weight = value

    @property
    def height(self):
        return self._height

    @height.setter
    def height(self, value):
        if value <= 0:
            raise ValueError("Height must be greater than zero.")
        self._height = value

    @abstractmethod
    def calculate_bmi(self):
        pass

    @abstractmethod
    def get_bmi_category(self):
        pass

    def print_info(self):
        print(f"Name: {self.name}")
        print(f"Age: {self.age}")
        print(f"Weight: {self.weight} kg")
        print(f"Height: {self.height} m")
        print(f"BMI: {self.calculate_bmi():.2f}")
        print(f"Category: {self.get_bmi_category()}")
        print("-" * 30)


# Adult class inheriting Person
class Adult(Person):
    def calculate_bmi(self):
        return self.weight / (self.height ** 2)

    def get_bmi_category(self):
        bmi = self.calculate_bmi()
        if bmi < 18.5:
            return "Underweight"
        elif 18.5 <= bmi < 24.9:
            return "Normal weight"
        elif 24.9 <= bmi < 29.9:
            return "Overweight"
        else:
            return "Obese"


# Child class inheriting Person
class Child(Person):
    def calculate_bmi(self):
        # BMI for children has an adjustment factor based on age
        bmi = self.weight / (self.height ** 2)
        if self.age < 2:
            return bmi * 1.5  # Adjustment for very young children
        elif self.age < 5:
            return bmi * 1.3  # Adjustment for children below 5
        return bmi

    def get_bmi_category(self):
        bmi = self.calculate_bmi()
        if bmi < 14:
            return "Underweight"
        elif 14 <= bmi < 18:
            return "Normal weight"
        elif 18 <= bmi < 24:
            return "Overweight"
        else:
            return "Obese"


# BMIApp class to manage the program flow
class BMIApp:
    def __init__(self):
        self.people = []

    def add_person(self, person):
        self.people.append(person)

    def collect_user_data(self):
        name = input("Enter your name: ")
        age = int(input("Enter your age: "))
        weight = float(input("Enter your weight in kilograms: "))
        height = float(input("Enter your height in meters: "))

        if age >= 18:
            person = Adult(name, age, weight, height)
        else:
            person = Child(name, age, weight, height)

        self.add_person(person)

    def print_results(self):
        if self.people:
            for person in self.people:
                person.print_info()
        else:
            print("No person data to display.")

    def run(self):
        while True:
            self.collect_user_data()
            continue_input = input("Do you want to enter another person? (yes/no): ").strip().lower()
            if continue_input != 'yes':
                break
        self.print_results()


# Main execution
if __name__ == "__main__":
    app = BMIApp()
    app.run()
