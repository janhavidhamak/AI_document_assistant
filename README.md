# AI Abstractive Tutor (Local RAG)

An advanced, 100% local, privacy-first AI Document Assistant built using a Retrieval-Augmented Generation (RAG) architecture. 

Unlike standard RAG bots that simply copy-paste text from PDFs, this system is engineered to act as an **abstractive AI tutor**. It rewrites user queries for better understanding, fuses fragmented contexts mathematically, and generates entirely fresh, human-like explanations without relying on paid APIs or external servers.

## 🚀 Features
- **Total Data Privacy**: Runs 100% locally on your machine. No data is ever sent to OpenAI, Google, or any cloud server.
- **Intent-Driven Query Rewriting**: Vague user questions (e.g., "What does this mean?") are intercepted and rewritten into highly specific search queries before hitting the database.
- **Abstractive Generation**: Uses strict prompting and an optimal temperature (`0.7`) to prevent exact-sentence extraction, forcing the AI to summarize and explain concepts in its own words.
- **Context Fusion**: Cleans and deduplicates retrieved chunks (`k=5`) to give the LLM a massive, seamless context window without confusing overlaps.
- **Clean UI**: A fast, reactive Gradio web interface for PDF upload and chatting.

## 🛠️ Tech Stack
- **LangChain**: Core orchestration and RAG pipeline routing.
- **Ollama (`llama3.2:1b`)**: Local open-weights LLM used for both query rewriting and abstractive generation.
- **FAISS**: In-memory vector database for high-speed similarity search.
- **Sentence-Transformers**: (`all-MiniLM-L6-v2`) used to embed text locally.
- **Gradio**: Python frontend web framework.

## 📦 Installation & Setup

### 1. Install Ollama & The Model
Download and install [Ollama](https://ollama.com/).
Open your terminal and pull the lightweight Llama model:
```bash
ollama run llama3.2:1b
```

### 2. Clone the Repository
```bash
git clone https://github.com/janhavidhamak/AI_document_assistant.git
cd AI_document_assistant
```

### 3. Install Python Dependencies
```bash
pip install -r requirements.txt
```

## 🎮 Usage
1. Make sure Ollama is running in the background.
2. Start the application:
```bash
python app.py
```
3. Open the provided local URL (usually `http://127.0.0.1:7860`) in your web browser.
4. Upload any PDF file.
5. Wait for the success message, then ask the AI tutor a question!

## 📂 File Structure
- `app.py`: Main entry point and Gradio launcher.
- `rag.py`: The core RAG pipeline (Indexing, Retrieval, Query Rewriting, and Generation).
- `prompts.py`: The strict "rulebook" enforcing abstractive behavior over extraction.
- `utils.py`: Text chunk fusion and PDF loading utilities.
- `ui.py`: Frontend interface configuration.

## 💡 Why this over uploading to ChatGPT?
1. **Privacy**: Confidential documents (medical, legal, proprietary code) stay on your hard drive.
2. **Cost**: Zero API costs. Inference is free forever.
3. **No Black Boxes**: Full architectural control over chunk sizes, retrieval depth, and context compression.

---
*Built with Langchain, Ollama, and FAISS.*
