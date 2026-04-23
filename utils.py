from langchain_community.document_loaders import PyPDFLoader

def load_pdf(file):
    """
    Load a PDF from the given file path and return the documents.
    """
    loader = PyPDFLoader(file)
    documents = loader.load()
    return documents

def clean_and_fuse_chunks(docs):
    """
    Merge and clean retrieved chunks to avoid redundancy before passing to the final LLM prompt.
    This prevents the LLM from getting confused by overlapping chunk windows.
    """
    fused_text = []
    seen = set()
    
    for doc in docs:
        # Clean whitespaces and newlines
        clean_content = " ".join(doc.page_content.split())
        
        # Deduplicate identical or highly overlapping chunks
        if clean_content not in seen:
            seen.add(clean_content)
            fused_text.append(clean_content)
            
    # Return a clean fused context block separated by clear delimiters
    return "\n\n---\n\n".join(fused_text)
