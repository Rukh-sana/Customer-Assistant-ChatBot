import streamlit as st
import json
import faiss
import numpy as np
from sentence_transformers import SentenceTransformer
import logging
from groq_integration import GroqClient  # Importing existing GroqClient
import time
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Setup logging
logging.basicConfig(
    filename='chatbot_debug.log',
    filemode='a',
    format='%(asctime)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

# Constants
FAISS_INDEX_FILE = 'faiss_index.bin'
MAPPING_FILE = 'index_mapping.json'
MODEL_NAME = 'all-mpnet-base-v2'
MAX_TOKENS = 8100

# Initialize GroqClient
try:
    groq_client = GroqClient()
    logging.info("GroqClient initialized successfully.")
except Exception as e:
    logging.error(f"Error initializing GroqClient: {e}")
    st.error("Failed to initialize GroqClient. Please check the logs for more details.")

def generate_response(conversation_history: list, user_input: str) -> str:
    """
    Generate a response using the GroqClient AI model.
    """
    max_retries = 3
    backoff_factor = 2

    # Prepare the prompt for the AI model
    prompt = [
        {"role": "system", "content": "You are Moses, a helpful and professional customer support assistant."},
    ]

    # Add conversation history
    for message in conversation_history:
        if message.startswith("**You:**"):
            prompt.append({"role": "user", "content": message.replace("**You:**", "").strip()})
        elif message.startswith("**Bot:**"):
            prompt.append({"role": "assistant", "content": message.replace("**Bot:**", "").strip()})

    # Add the latest user input
    prompt.append({"role": "user", "content": user_input})

    for attempt in range(1, max_retries + 1):
        try:
            reply = groq_client.get_groq_response(
                messages=prompt,
                model="llama-3.2-90b-text-preview",
                temperature=0.7,
                max_tokens=512  # Max tokens for the response
            )
            return reply
        except Exception as e:
            logging.error(f"GroqClient error on attempt {attempt}: {e}")
            if attempt == max_retries:
                return "I'm experiencing technical difficulties. Please try again later."
            time.sleep(backoff_factor ** attempt)

@st.cache_resource
def load_faiss_index(index_file):
    try:
        index = faiss.read_index(index_file)
        logging.info(f"Loaded FAISS index from {index_file}")
    except Exception as e:
        logging.error(f"Error loading FAISS index: {e}")
        st.error("Failed to load FAISS index.")
        raise e
    return index

@st.cache_data
def load_mapping(mapping_file):
    try:
        with open(mapping_file, 'r', encoding='utf-8') as f:
            mapping = json.load(f)
        logging.info(f"Loaded mapping from {mapping_file}")
    except Exception as e:
        logging.error(f"Error loading mapping file: {e}")
        st.error("Failed to load mapping file.")
        raise e
    return mapping

@st.cache_resource
def initialize_model(model_name):
    try:
        model = SentenceTransformer(model_name)
        logging.info(f"Initialized SentenceTransformer model: {model_name}")
    except Exception as e:
        logging.error(f"Error initializing model: {e}")
        st.error("Failed to initialize the embedding model.")
        raise e
    return model

def find_intent(user_input, model, index, mapping, top_k=1):
    """
    Find the most similar intent based on user input using FAISS.
    """
    try:
        user_embedding = model.encode([user_input], convert_to_numpy=True).astype('float32')
        distances, indices = index.search(user_embedding, top_k)
        best_match_idx = indices[0][0]
        best_distance = distances[0][0]

        # Define a similarity threshold (adjust based on empirical results)
        similarity_threshold = 1000  # Adjust this threshold based on your dataset

        if best_distance < similarity_threshold:
            matched_entry = mapping[best_match_idx]
            logging.info(f"Matched intent: {matched_entry['intent']} | {matched_entry['sub_intent']}")
            return matched_entry
        else:
            logging.info("No intent matched based on similarity threshold.")
            return None
    except Exception as e:
        logging.error(f"Error in find_intent: {e}")
        return None

def evaluate_condition(condition, user_reply):
    """
    Evaluate if the user's reply satisfies the condition.
    """
    if condition.lower() in user_reply.lower():
        return True
    return False

def get_next_response(current_step, responses, user_reply=None):
    """
    Get the next response based on the current step and user reply.
    """
    for response in responses:
        if response['step'] == current_step:
            if 'condition' in response:
                if user_reply and evaluate_condition(response['condition'], user_reply):
                    return response['message'], current_step + 1
            else:
                return response['message'], current_step + 1
    return "I'm sorry, something went wrong.", current_step

def reset_conversation():
    """
    Reset the conversation state.
    """
    st.session_state.conversation = []
    st.session_state.current_intent = None
    st.session_state.current_sub_intent = None
    st.session_state.current_step = 1

def main():
    st.set_page_config(page_title="Customer Support Chatbot", page_icon="💬", layout="wide")
    st.markdown(
        """
        <style>
        .chat-container {
            max-width: 700px;
            margin: 0 auto;
        }
        .user-message {
            background-color: #DCF8C6;
            padding: 10px;
            border-radius: 10px;
            margin-bottom: 5px;
            text-align: right;
            word-wrap: break-word;
        }
        .bot-message {
            background-color: #F1F0F0;
            padding: 10px;
            border-radius: 10px;
            margin-bottom: 5px;
            text-align: left;
            word-wrap: break-word;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )

    st.markdown("<h1 style='text-align: center;'>💬 Customer Support Chatbot</h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center;'>Hello! I'm Moses, your customer support assistant. How can I help you today?</p>", unsafe_allow_html=True)

    # Load FAISS index and mapping
    index = load_faiss_index(FAISS_INDEX_FILE)
    mapping = load_mapping(MAPPING_FILE)
    model = initialize_model(MODEL_NAME)

    # Verify that GROQ_API_KEY is loaded
    groq_api_key = os.getenv('GROQ_API_KEY')
    if not groq_api_key:
        logging.error("GROQ_API_KEY not found. Please check your .env file.")
        st.error("Configuration error: GROQ_API_KEY not found.")
        return

    # Initialize session state for conversation and tracking
    if 'conversation' not in st.session_state:
        st.session_state.conversation = []
    if 'current_intent' not in st.session_state:
        st.session_state.current_intent = None
    if 'current_sub_intent' not in st.session_state:
        st.session_state.current_sub_intent = None
    if 'current_step' not in st.session_state:
        st.session_state.current_step = 1

    # Display the updated conversation
    st.markdown("<div class='chat-container'>", unsafe_allow_html=True)
    for msg in st.session_state.conversation:
        if msg.startswith("**You:**"):
            st.markdown(f"<div class='user-message'>{msg.replace('**You:**', '').strip()}</div>", unsafe_allow_html=True)
        elif msg.startswith("**Bot:**"):
            st.markdown(f"<div class='bot-message'>{msg.replace('**Bot:**', '').strip()}</div>", unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)

    # Message input and send button in a form
    with st.form(key='message_form', clear_on_submit=True):
        col1, col2 = st.columns([8,1])
        with col1:
            user_input = st.text_input("Type your message here...", key="user_input", label_visibility='collapsed')
        with col2:
            submitted = st.form_submit_button('Send')

        if submitted:
            if user_input:
                # Append user message to conversation
                st.session_state.conversation.append(f"**You:** {user_input}")
                logging.info(f"User input: {user_input}")

                if st.session_state.current_intent is None:
                    # Find intent based on user input
                    matched = find_intent(user_input, model, index, mapping, top_k=1)
                    if matched:
                        st.session_state.current_intent = matched['intent']
                        st.session_state.current_sub_intent = matched['sub_intent']
                        responses = matched['responses']
                        # Get the first response
                        response_message, next_step = get_next_response(1, responses)
                        st.session_state.conversation.append(f"**Bot:** {response_message}")
                        logging.info(f"Bot response: {response_message}")
                        st.session_state.current_step = next_step
                    else:
                        # If no intent matched, use GroqClient to generate a response
                        conversation_history = st.session_state.conversation.copy()
                        groq_response = generate_response(conversation_history, user_input)
                        st.session_state.conversation.append(f"**Bot:** {groq_response}")
                        logging.info(f"Bot (GroqClient) response: {groq_response}")
                else:
                    # Continue the conversation based on current intent and step
                    try:
                        # Retrieve the current matched entry
                        current_entry = next(
                            (item for item in mapping if item['intent'] == st.session_state.current_intent and item['sub_intent'] == st.session_state.current_sub_intent),
                            None
                        )
                        if current_entry:
                            responses = current_entry['responses']
                            response_message, next_step = get_next_response(st.session_state.current_step, responses, user_input)
                            st.session_state.conversation.append(f"**Bot:** {response_message}")
                            logging.info(f"Bot response: {response_message}")
                            st.session_state.current_step = next_step

                            # Handle final step by resetting the conversation
                            if st.session_state.current_step > len(responses):
                                reset_conversation()
                        else:
                            st.session_state.conversation.append("**Bot:** I'm sorry, I couldn't retrieve the context. Let's start over.")
                            logging.warning("Current intent not found in mapping.")
                            reset_conversation()
                    except Exception as e:
                        logging.error(f"Error during conversation continuation: {e}")
                        st.session_state.conversation.append("**Bot:** I'm sorry, something went wrong. Let's start over.")
                        reset_conversation()

    # File upload for feedback
    st.markdown("If you'd like to upload feedback or a file, you can do so below:")
    uploaded_file = st.file_uploader("Upload a PDF or DOC file", type=['pdf', 'doc', 'docx'])
    if uploaded_file:
        # Handle file upload
        file_details = {"filename": uploaded_file.name, "filetype": uploaded_file.type, "filesize": uploaded_file.size}
        logging.info(f"Uploaded file: {file_details}")
        st.session_state.conversation.append(f"**You have uploaded a file named {uploaded_file.name}**")
        st.success(f"File '{uploaded_file.name}' uploaded successfully.")
        # You can add code here to process the file as needed

        # Display the updated conversation
        st.markdown("<div class='chat-container'>", unsafe_allow_html=True)
        for msg in st.session_state.conversation:
            if msg.startswith("**You:**"):
                st.markdown(f"<div class='user-message'>{msg.replace('**You:**', '').strip()}</div>", unsafe_allow_html=True)
            elif msg.startswith("**Bot:**"):
                st.markdown(f"<div class='bot-message'>{msg.replace('**Bot:**', '').strip()}</div>", unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)

if __name__ == "__main__":
    main()