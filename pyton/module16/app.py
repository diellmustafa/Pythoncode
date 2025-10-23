import streamlit as st

def main():
    st.title("Hello World!")
    if st.button("Click me!"):
        st.write("Button Clicked!")
    if st.checkbox("Check me!"):
        st.write("Box checked!")
    user_input = st.text_input("Enter Text", "Sample Text")
    st.write("You entered:", user_input)
    age = st.number_input("enter your age:", min_value=0, max_value=100)
    st.write("You entered", age)
    message = st.text_area("Enter a messsage: ")
    st.write(f"Your message: {message}")
    choice = st.radio("Pick one:", ["Choice1", "Choice2", "Choice3"])
    st.write(f"You chose: {choice}")
    if st.button("Succeess"):
        st.success("Operation was successful")
    try:
        1/0
    except Exception as e:
        st.exception(e)


if __name__ == "__main__":
    main()



#RUN IN TERMINAL:
#streamlit run module16/app.py
#    FILE NAME ^^^^^^^^^^^^^^^