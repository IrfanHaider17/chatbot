import os  # Add this import at the top
import requests
import gradio as gr

# Read the Groq API key from the environment variable
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

# Correct Groq API endpoint
GROQ_API_URL = "https://api.groq.com/openai/v1/chat/completions"

# Function to send a message to the Groq API
def send_message_to_groq(message):
    headers = {
        "Authorization": f"Bearer {GROQ_API_KEY}",
        "Content-Type": "application/json"
    }
    
    data = {
        "model": "mixtral-8x7b-32768",  # Replace with the correct model name
        "messages": [{"role": "user", "content": message}],
        "temperature": 0.7,
        "max_tokens": 150
    }
    
    response = requests.post(GROQ_API_URL, headers=headers, json=data)
    
    if response.status_code == 200:
        return response.json()["choices"][0]["message"]["content"]
    else:
        return f"Error: {response.status_code}, {response.text}"

# Function to handle Gradio interface interaction
def chatbot_interface(input_text):
    if input_text.strip().lower() == "exit":
        return "Goodbye! Chat session ended."
    response = send_message_to_groq(input_text)
    return response

# Gradio interface setup
def create_gradio_interface():
    interface = gr.Interface(
        fn=chatbot_interface,  # Function to call
        inputs="text",         # Input type
        outputs="text",        # Output type
        title="Groq Chatbot",  # Title of the interface
        description="A chatbot powered by Groq API. Type your message and press Enter.",
        live=False             # Disable live updates (press Enter to submit)
    )
    return interface

# Run the Gradio interface
if __name__ == "__main__":
    interface = create_gradio_interface()
    interface.launch()  # Launches the Gradio app
