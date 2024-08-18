import streamlit as st

st.title("Streamlit Test Application")

st.write("Hello, this is a test application using Streamlit!")

user_input = st.text_input("Enter something:")

st.write(f"You entered: {user_input}")

st.line_chart([1, 2, 3, 4, 5])
