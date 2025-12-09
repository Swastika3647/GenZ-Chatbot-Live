import streamlit as st
import google.generativeai as genai
import random

# Page Config
st.set_page_config(page_title="GenZ AI Bestie", page_icon="✨")

# Title and Caption
st.title("✨ GenZ AI Bestie")
st.caption("No cap, I'm just an AI. Ask me anything, bestie! 💅")

# --- MEME COLLECTION (The "Database") ---
GENZ_MEMES = [
    "https://i.imgflip.com/7n5z56.jpg",  # Side eye
    "https://i.imgflip.com/8k94w.jpg",   # This is fine
    "https://i.imgflip.com/26am.jpg",    # Aliens guy
    "https://i.imgflip.com/1h7in3.jpg",  # Mocking SpongeBob
    "https://i.imgflip.com/9ehk.jpg",    # Disaster Girl
    "https://i.imgflip.com/1bij.jpg",    # Batman slap
    "https://media.giphy.com/media/v1.Y2lkPTc5MGI3NjExM3Z5Z3p5Z3Z5Z3Z5Z3Z5Z3Z5Z3Z5Z3Z5Z3Z5/l3q2K5jinAlChoCLS/giphy.gif" # Slay gif
]

# --- SECURE API KEY HANDLING ---
try:
    if "GEMINI_API_KEY" in st.secrets:
        api_key = st.secrets["GEMINI_API_KEY"]
    else:
        with st.sidebar:
            st.header("Settings")
            api_key = st.text_input("Enter your Gemini API Key", type="password")
            st.markdown("[Get your API key here](https://aistudio.google.com/app/apikey)")
except FileNotFoundError:
    with st.sidebar:
        st.header("Settings")
        api_key = st.text_input("Enter your Gemini API Key", type="password")
        st.markdown("[Get your API key here](https://aistudio.google.com/app/apikey)")

# Initialize Chat History
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display Chat History
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        # Check if the message contains the secret MEME code
        if "[SEND_MEME]" in message["content"]:
            # Display the text part
            clean_text = message["content"].replace("[SEND_MEME]", "")
            st.write(clean_text)
            # Display a random meme (simulated)
            # In a real app, you would store the specific image URL in history
            st.image(random.choice(GENZ_MEMES), width=300)
        else:
            st.write(message["content"])

# Function to get response from Gemini
def get_gemini_response(user_prompt, key):
    try:
        genai.configure(api_key=key)
        
        # --- UPDATED SYSTEM PROMPT (The "Tool Use" Instruction) ---
        system_instruction = """
        You are a Gen Z teenager. 
        - You use slang like 'no cap', 'bet', 'slay', 'sus', 'fr', 'goated', 'mid'.
        - You type mostly in lowercase but use CAPS for emphasis.
        - You are helpful but keep it casual and chill.
        
        IMPORTANT TOOL INSTRUCTION:
        - If the user explicitly asks for a meme (e.g., "send me a meme", "show me something funny"), 
        - OR if the vibe is right for a reaction image,
        - You must include the text "[SEND_MEME]" at the end of your response.
        """
        
        # Using the model that worked for you
        model = genai.GenerativeModel("gemini-2.5-flash")
        
        # Combine history
        chat_history = []
        chat_history.append({"role": "user", "parts": [system_instruction]})
        
        for msg in st.session_state.messages:
            role = "user" if msg["role"] == "user" else "model"
            # We strip the code from history so the model doesn't get confused
            clean_content = msg["content"].replace("[SEND_MEME]", "") 
            chat_history.append({"role": role, "parts": [clean_content]})
        
        chat_history.append({"role": "user", "parts": [user_prompt]})

        response = model.generate_content(chat_history)
        return response.text
    except Exception as e:
        return f"Bruh, something went wrong: {str(e)}"

# User Input
if prompt := st.chat_input("Spill the tea..."):
    if not api_key:
        st.info("Bestie, I need an API key to work! 🔑")
        st.stop()

    # Add user message
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.write(prompt)

    # Generate Response
    with st.chat_message("assistant"):
        with st.spinner("Thinking... 🤔"):
            response_text = get_gemini_response(prompt, api_key)
            
            # Check for the meme code immediately
            if "[SEND_MEME]" in response_text:
                clean_text = response_text.replace("[SEND_MEME]", "")
                st.write(clean_text)
                st.image(random.choice(GENZ_MEMES), caption="Mood 💅", width=300)
            else:
                st.write(response_text)
    
    # Add assistant response to session state
    st.session_state.messages.append({"role": "assistant", "content": response_text})