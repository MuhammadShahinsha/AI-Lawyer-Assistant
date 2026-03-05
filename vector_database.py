<<<<<<< HEAD
import os
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS
from langchain_huggingface import HuggingFaceEmbeddings

# Permanent FAISS storage path
FAISS_PATH = "faiss_index"
DATA_FOLDER = "data"  # Folder containing all your PDFs
embedding_model = HuggingFaceEmbeddings(
    model_name="sentence-transformers/all-MiniLM-L6-v2"
)


def get_embedding_model():
    """Load Hugging Face embedding model."""
    return embedding_model


def load_or_create_faiss():
    """Load existing FAISS index or create a new one from /data PDFs."""
    embedding_model = get_embedding_model()

    if os.path.exists(FAISS_PATH):
        print("📂 Loading existing FAISS database...")
        return FAISS.load_local(FAISS_PATH, embedding_model, allow_dangerous_deserialization=True)

    print("⚙️ No FAISS index found — creating new one from PDFs...")
    pdf_files = [f for f in os.listdir(DATA_FOLDER) if f.lower().endswith(".pdf")]
    if not pdf_files:
        raise FileNotFoundError("❌ No PDF files found in the 'data' folder!")
    #goes through each pdf using pypdfloader.
    docs = []
    for pdf_file in pdf_files:
        path = os.path.join(DATA_FOLDER, pdf_file)
        print(f"📄 Loading: {pdf_file}")
        loader = PyPDFLoader(path)
        docs.extend(loader.load())
    #each document split into small chunks (1500)
    splitter = RecursiveCharacterTextSplitter(chunk_size=1500, chunk_overlap=200)
    chunks = splitter.split_documents(docs)

    print("🔢 Creating FAISS embeddings...")
    faiss_db = FAISS.from_documents(chunks, embedding_model)
    faiss_db.save_local(FAISS_PATH)
    print("✅ FAISS index created and saved successfully!")

    return faiss_db


def similarity_search(query, k=3):
    """Retrieve top-k similar documents for a query."""
    embedding = get_embedding_model()
    if not os.path.exists(FAISS_PATH):
        raise FileNotFoundError("⚠️ FAISS database not found. Please run vector_database.py once.")
    db = FAISS.load_local(FAISS_PATH, embedding, allow_dangerous_deserialization=True)
    return db.similarity_search(query, k=k)


if __name__ == "__main__":
    print("🧠 Initializing FAISS from permanent PDFs...")
    load_or_create_faiss()
=======
import os
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS
from langchain_ollama import OllamaEmbeddings

# Permanent FAISS storage path
FAISS_PATH = "faiss_index"
DATA_FOLDER = "data"  # Folder containing all your PDFs
OLLAMA_MODEL_NAME = "nomic-embed-text"#used by ollama to turn text to vectors.


def get_embedding_model(model_name=OLLAMA_MODEL_NAME):
    """Load Ollama embedding model."""
    return OllamaEmbeddings(model=model_name)


def load_or_create_faiss():
    """Load existing FAISS index or create a new one from /data PDFs."""
    embedding_model = get_embedding_model()

    if os.path.exists(FAISS_PATH):
        print("📂 Loading existing FAISS database...")
        return FAISS.load_local(FAISS_PATH, embedding_model, allow_dangerous_deserialization=True)

    print("⚙️ No FAISS index found — creating new one from PDFs...")
    pdf_files = [f for f in os.listdir(DATA_FOLDER) if f.lower().endswith(".pdf")]
    if not pdf_files:
        raise FileNotFoundError("❌ No PDF files found in the 'data' folder!")
    #goes through each pdf using pypdfloader.
    docs = []
    for pdf_file in pdf_files:
        path = os.path.join(DATA_FOLDER, pdf_file)
        print(f"📄 Loading: {pdf_file}")
        loader = PyPDFLoader(path)
        docs.extend(loader.load())
    #each document split into small chunks (1500)
    splitter = RecursiveCharacterTextSplitter(chunk_size=1500, chunk_overlap=200)
    chunks = splitter.split_documents(docs)

    print("🔢 Creating FAISS embeddings...")
    faiss_db = FAISS.from_documents(chunks, embedding_model)
    faiss_db.save_local(FAISS_PATH)
    print("✅ FAISS index created and saved successfully!")

    return faiss_db


def similarity_search(query, k=3):
    """Retrieve top-k similar documents for a query."""
    embedding = get_embedding_model()
    if not os.path.exists(FAISS_PATH):
        raise FileNotFoundError("⚠️ FAISS database not found. Please run vector_database.py once.")
    db = FAISS.load_local(FAISS_PATH, embedding, allow_dangerous_deserialization=True)
    return db.similarity_search(query, k=k)


if __name__ == "__main__":
    print("🧠 Initializing FAISS from permanent PDFs...")
    load_or_create_faiss()
>>>>>>> 5501faa62b9e26c8562e578b0bb730c8bc28d76f
