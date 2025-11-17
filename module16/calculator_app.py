import streamlit as st

def calculate(num1, num2, operation):
    if operation == "Addition":
        result = num1 + num2
    elif operation == "Subtraction":
        result = num1 - num2
    elif operation == "Multiplication":
        result = num1 * num2
    elif operation == "Division":
        try:
            result = num1 / num2
        except ZeroDivisionError:
            result = "Cannot divide by zero"
    return result

def main():
    st.title("Simple Calculator")
    num1 = st.number_input("Enter the first number: ")
    num2 = st.number_input("Enter the second number: ")
    operation = st.radio("Select operation: ", ["Addition", "Subtraction", "Addition", "Division"])
    result = calculate(num1, num2, operation)
    st.write(f"Your result is: {result}")

if __name__ == "__main__":
    main()