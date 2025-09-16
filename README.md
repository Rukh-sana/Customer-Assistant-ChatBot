# 🤖 Customer Assistant ChatBot

An **AI-powered Customer Support ChatBot** built with **Streamlit**, **FAISS**, **Sentence Transformers**, and **Groq LLMs**, designed to provide professional, context-aware, and intent-driven conversations.

---

## 🚀 Features
- **Streamlit UI** – Simple, interactive, and user-friendly interface.
- **FAISS Integration** – Efficient vector similarity search for knowledge retrieval.
- **Sentence Transformers** – Embeddings for semantic understanding.
- **Groq LLMs** – Seamless integration with Groq’s API for conversational intelligence.
- **Custom Persona & Question Bank** – Easily configurable chatbot behavior.
- **Logging System** – Debug and monitor chatbot responses.
- **Configurable Storage** – JSON-based configuration for flexible use.

---

## 📂 Project Structure

---
Chatbot/

│── main.py # Streamlit app entry point/
│── groq_integration.py # Groq API integration/
│── faiss_index.bin # FAISS vector index
│── persona.json # Bot personality configuration
│── question_bank.json # Predefined Q&A pairs
│── chatbot_debug.log # Debug logs
│── .github/workflows/ # CI/CD workflows

## ⚙️ Installation
Clone the repository and create a virtual environment:

```bash
git clone https://github.com/Rukh-sana/Customer-Assistant-ChatBot.git
cd Customer-Assistant-ChatBot

# Create virtual environment
python -m venv .venv
source .venv/bin/activate   # On Windows: .venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

