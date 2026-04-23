import os
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.chat_models import ChatOllama
from langchain_core.output_parsers import StrOutputParser

from prompts import QUERY_REWRITE_PROMPT, ABSTRACTIVE_QA_PROMPT
from utils import clean_and_fuse_chunks

DB_FAISS_PATH = "faiss_index"

def process_documents(docs):
    """
    Splits documents into chunks, generates embeddings, and stores them in FAISS.
    """

    text_splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)
    chunks = text_splitter.split_documents(docs)
    
    embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
    
    # Store embeddings in FAISS vectorstore
    vectorstore = FAISS.from_documents(chunks, embeddings)
    
    # Save the vectorstore locally
    vectorstore.save_local(DB_FAISS_PATH)
    
    return "PDF successfully processed and stored."


def get_answer(query):
    """
    Retrieves the most relevant chunks, fuses them, and generates an abstractive answer.
    """
    embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
    
    if not os.path.exists(DB_FAISS_PATH):
        return "Index not found. Please upload a PDF first.", "N/A"
        
    vectorstore = FAISS.load_local(DB_FAISS_PATH, embeddings, allow_dangerous_deserialization=True)
    
    # Initialize the generative LLM using local Ollama
    llm = ChatOllama(model="llama3.2:1b", temperature=0.7)
    

    rewrite_chain = QUERY_REWRITE_PROMPT | llm | StrOutputParser()
    try:
        rewritten_query = rewrite_chain.invoke({"question": query})
        print(f"\n[DEBUG] Original Query: {query}")
        print(f"[DEBUG] Rewritten Intent: {rewritten_query}\n")
    except Exception as e:
        return f"Ollama Connection Error: {str(e)}\n\nPlease ensure Ollama is installed, running, and you have downloaded the llama3 model (run 'ollama run llama3' in terminal).", "N/A"
        
 
    docs = vectorstore.similarity_search(rewritten_query, k=5)
    
    if not docs:
        return "No relevant information found.", "N/A"
        
   
    fused_context = clean_and_fuse_chunks(docs)
    
    # Extract unique page numbers
    page_numbers = sorted(list(set([doc.metadata.get("page", -1) for doc in docs if doc.metadata.get("page", -1) != -1])))
    pages_str = ", ".join([str(p + 1) for p in page_numbers]) if page_numbers else "Unknown"
    
  
    qa_chain = ABSTRACTIVE_QA_PROMPT | llm | StrOutputParser()
    
  
    final_answer = qa_chain.invoke({
        "context": fused_context,
        "question": query  
    })
    
    return final_answer, pages_str
