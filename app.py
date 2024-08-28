import streamlit as st
import google.generativeai as genai

# Set your API key directly (replace 'YOUR_API_KEY' with your actual API key)
api_key = "AIzaSyBUskQVX8HQsSYwOP8PCpTXgvqu8SG-2KA"

# Configure Generative AI with your API key
genai.configure(api_key=api_key)

## function to load Gemini Pro model and get responses
model = genai.GenerativeModel("gemini-pro")
chat = model.start_chat(history=[])

def get_gemini_response(question):
    response = chat.send_message(question, stream=True)
    return response

def main():
    st.title("Code-GENERATOR")
    st.write("Input: ")

    chat_history = []

    while True:
        input_text = st.text_input("You:", key=f"input_field_{len(chat_history)}")
        if not input_text:
            break

        response = get_gemini_response(input_text)
        st.write("The Response is:")
        for chunk in response:
            try:
                if hasattr(chunk, 'text'):
                    st.write(chunk.text)
                    chat_history.append(("Bot", chunk.text))
                else:
                    st.write("Response does not contain valid text.")
            except Exception as e:
                st.write(f"An error occurred: {e}")

        chat_history.append(("You", input_text))

    st.write("The Chat History is:")
    for role, text in chat_history:
        st.write(f"{role}: {text}")

if __name__ == "__main__":
    main()
