import streamlit as st
import google.generativeai as genai

# Set your API key directly (replace 'YOUR_API_KEY' with your actual API key)
api_key = "AIzaSyA6-dMd5wrgEFRJzL-W1RkIhhp_15AD3tA"

# Configure Generative AI with your API key
genai.configure(api_key=api_key)

# Load the Gemini Pro model and start a chat session
model = genai.GenerativeModel("gemini-pro")
chat = model.start_chat(history=[])

# Function to get responses from the Gemini Pro model
def get_gemini_response(question):
    try:
        # Validate input
        if not isinstance(question, str) or not question.strip():
            raise ValueError("Invalid question. It must be a non-empty string.")
        
        # Send the message to the model
        response = chat.send_message(question, stream=True)
        return response
    
    except google.api_core.exceptions.InvalidArgument as e:
        st.error("Invalid argument provided to the API. Please check your input.")
        st.error(f"Error details: {str(e)}")
        return None
    
    except Exception as e:
        st.error(f"An unexpected error occurred: {str(e)}")
        return None

# Main function to run the Streamlit app
def main():
    st.title("Code-GENERATOR")
    st.write("Input: ")

    chat_history = []

    while True:
        input_text = st.text_input("You:", key=f"input_field_{len(chat_history)}")
        if not input_text:
            break

        # Get the response from the Gemini API
        response = get_gemini_response(input_text)
        
        if response:
            st.write("The Response is:")
            for chunk in response:
                try:
                    if hasattr(chunk, 'text'):
                        st.write(chunk.text)
                        chat_history.append(("Bot", chunk.text))
                    else:
                        st.write("Response does not contain valid text.")
                except Exception as e:
                    st.write(f"An error occurred while processing the response: {e}")
        
        chat_history.append(("You", input_text))

    st.write("The Chat History is:")
    for role, text in chat_history:
        st.write(f"{role}: {text}")

if __name__ == "__main__":
    main()
