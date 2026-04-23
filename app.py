import os
from dotenv import load_dotenv
from utils import load_pdf
from rag import process_documents, get_answer
from ui import create_ui

# Load environment variables (.env file) if any
load_dotenv()

def handle_upload(file_path):
    """
    Callback when PDF is uploaded.
    """
    if not file_path:
        return "Please provide a valid file."
        
    try:
        docs = load_pdf(file_path)
        status = process_documents(docs)
        return status
    except Exception as e:
        return f"Error processing PDF: {str(e)}"

def handle_question(question):
    """
    Callback when a question is asked.
    """
    if not question.strip():
        return "Please enter a question.", "N/A"
    
    try:
        answer, page = get_answer(question)
        return answer, page
    except Exception as e:
        return f"Error getting answer: {str(e)}\n\nDid you make sure Ollama is running?", "N/A"

if __name__ == "__main__":
    print("Starting AI Tutor Assistant (Local Ollama Version)...")
    
    # Create the UI and pass the handler functions
    demo = create_ui(handle_upload, handle_question)
    
    # Launch the app
    demo.launch()
