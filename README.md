# 🤖 Customer Assistant ChatBot

[![Python](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/)  
[![Streamlit](https://img.shields.io/badge/Streamlit-App-red?logo=streamlit)](https://streamlit.io/)  
[![FAISS](https://img.shields.io/badge/FAISS-Vector%20Search-green)](https://faiss.ai/)  
[![GitHub Actions](https://img.shields.io/github/actions/workflow/status/Rukh-sana/Customer-Assistant-ChatBot/python-publish.yml?branch=main&label=build&logo=github)](https://github.com/Rukh-sana/Customer-Assistant-ChatBot/actions)  
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)  

A **Streamlit-based AI Customer Assistant** powered by **Groq API** and **FAISS vector search**, designed to provide fast and intelligent responses to customer queries.  
This chatbot supports a **custom persona**, predefined Q&A pairs, and integrates modern NLP embeddings for context-aware conversations.  

---

## 📸 Screenshots

| Chat Interface | Debug Logs |  
|----------------|------------|  
| ![Chatbot UI](screenshots/chat_ui.png) | ![Logs](screenshots/debug_logs.png) |  

---

## 🏷️ Keywords

`Chatbot` · `AI Assistant` · `Streamlit` · `Groq API` · `FAISS` · `Sentence Transformers` · `Customer Support` · `NLP` · `Machine Learning`  

---

## 📑 Table of Contents

- [✨ Features](#-features)  
- [📂 Project Structure](#-project-structure)  
- [⚙️ Installation](#️-installation)  
- [▶️ Usage](#️-usage)  
- [🧩 Configuration](#-configuration)  
- [🛠 Tech Stack](#-tech-stack)  
- [🤝 Contribution](#-contribution)  
- [📜 License](#-license)  
- [👩‍💻 Author](#-author)  

---

## ✨ Features

- 🧠 **AI-Powered Responses** using Groq API  
- 📂 **FAISS Vector Search** for similarity matching  
- 🎭 **Custom Persona** via `persona.json`  
- ❓ **Predefined Q&A** with `question_bank.json`  
- 🖥 **Streamlit Web Interface** for easy interaction  
- 🛠 **Debug Logging** to trace issues in `chatbot_debug.log`  
- 🚀 **CI/CD Workflows** with GitHub Actions  

---



## 📸 Screenshots

| Chat Interface | Debug Logs |  
|----------------|------------|  
| ![Chatbot UI](screenshots/chat_ui.png) | ![Logs](screenshots/debug_logs.png) |  

---

## 🏷️ Keywords

`Chatbot` · `AI Assistant` · `Streamlit` · `Groq API` · `FAISS` · `Sentence Transformers` · `Customer Support` · `NLP` · `Machine Learning`  

---

## 📑 Table of Contents

- [✨ Features](#-features)  
- [📂 Project Structure](#-project-structure)  
- [⚙️ Installation](#️-installation)  
- [▶️ Usage](#️-usage)  
- [🧩 Configuration](#-configuration)  
- [🛠 Tech Stack](#-tech-stack)  
- [🤝 Contribution](#-contribution)  
- [📜 License](#-license)  
- [👩‍💻 Author](#-author)  

---

## ✨ Features

- 🧠 **AI-Powered Responses** using Groq API  
- 📂 **FAISS Vector Search** for similarity matching  
- 🎭 **Custom Persona** via `persona.json`  
- ❓ **Predefined Q&A** with `question_bank.json`  
- 🖥 **Streamlit Web Interface** for easy interaction  
- 🛠 **Debug Logging** to trace issues in `chatbot_debug.log`  
- 🚀 **CI/CD Workflows** with GitHub Actions  

---

## 📂 Project Structure

```

Chatbot/
│── main.py              # Streamlit app entry point
│── groq\_integration.py  # Groq API integration
│── faiss\_index.bin      # FAISS vector index
│── persona.json         # Bot personality configuration
│── question\_bank.json   # Predefined Q\&A pairs
│── chatbot\_debug.log    # Debug logs
│── .github/workflows/   # CI/CD workflows

````

---

## ⚙️ Installation

Clone the repository and create a virtual environment:

```bash
git clone https://github.com/Rukh-sana/Customer-Assistant-ChatBot.git
cd Customer-Assistant-ChatBot

# Create virtual environment
python -m venv .venv
source .venv/bin/activate   # On Windows: .venv\Scripts\activate
````

Install dependencies:

```bash
pip install -r requirements.txt
```

---

## ▶️ Usage

Run the Streamlit app:

```bash
streamlit run main.py
```

The chatbot will launch in your browser at `http://localhost:8501`.

---

## 🧩 Configuration

* **Persona settings:** Customize `persona.json` to change chatbot tone and style.
* **Knowledge base:** Update `question_bank.json` with more Q\&A pairs.
* **Vector index:** Regenerate `faiss_index.bin` if you add new embeddings.

---

## 🛠 Tech Stack

* [Python 3.10+](https://www.python.org/)
* [Streamlit](https://streamlit.io/) – Web UI
* [FAISS](https://faiss.ai/) – Vector similarity search
* [Sentence Transformers](https://www.sbert.net/) – Embedding model
* [Groq API](https://groq.com/) – LLM integration
* [GitHub Actions](https://docs.github.com/en/actions) – CI/CD

---

## 🤝 Contribution

Contributions are welcome!

1. Fork the repository
2. Create a new branch (`feature/my-feature`)
3. Commit your changes
4. Push to the branch
5. Open a Pull Request

---

## 📜 License

This project is licensed under the **MIT License**.
See the [LICENSE](LICENSE) file for details.

---

