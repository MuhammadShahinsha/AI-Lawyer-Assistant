from langchain_groq import ChatGroq
from vector_database import similarity_search
from langchain_core.prompts import ChatPromptTemplate
from langchain_community.document_loaders import PyPDFLoader


#  Step 1: Setup LLM (Meta Llama via Groq)
llm_model = ChatGroq(model="llama-3.3-70b-versatile")


# Step 2: Extract text from uploaded case file (e.g., FIR, charge sheet)
def extract_case_text(uploaded_file):
    """
    Extracts text from a user-uploaded PDF case report using PyPDFLoader.
    """
    import os
    #Saves the uploaded user file temporarily for text extraction.
    os.makedirs("uploaded_cases", exist_ok=True)
    file_path = os.path.join("uploaded_cases", uploaded_file.name)

    # Save file temporarily
    with open(file_path, "wb") as f:
        f.write(uploaded_file.getbuffer())
    #to extract user uploaded page.
    loader = PyPDFLoader(file_path)
    docs = loader.load()

    # Combine all text from PDF pages
    full_text = "\n\n".join([doc.page_content for doc in docs])
    return full_text


#  Step 3: Retrieve similar legal documents from FAISS
def retrieve_docs(query):
    return similarity_search(query)


def get_context(documents):
    """
    Joins retrieved documents into a single context string.
    """
    if not documents:
        return "No relevant documents found in the legal database."
    return "\n\n".join([doc.page_content for doc in documents])


#  Step 4: Define custom prompt for the AI lawyer.defines how the AI should think and answer.
custom_prompt_template = """
You are an experienced Indian criminal lawyer.

Use the information from the **context** (legal references like IPC, CrPC, etc.)
and the **case text** (uploaded FIR or case report) to give a detailed but concise answer.

Follow these rules:
- Base your answer strictly on the provided documents and case file.
- If you are not sure, say you don't know.
- Explain what legal sections are involved and what actions the user should consider next.
- Keep the tone professional and simple.

---

📄 **Case Report:**
{case_text}

📚 **Legal Context:**
{context}

❓ **Question:**
{question}

💬 **Answer (in plain language):**
"""


#  Step 5: Generate the AI’s response
def answer_query(question, case_text, model):
    """
    Combines the case text and retrieved legal docs to generate a clear legal answer.
    """
    documents = retrieve_docs(question)
    context = get_context(documents)
    prompt = ChatPromptTemplate.from_template(custom_prompt_template)
    chain = prompt | model

    result = chain.invoke({
        "question": question,
        "context": context,
        "case_text": case_text
    })

    #  Return only the pure text (no metadata)
    if hasattr(result, "content"):
        return result.content.strip()
    else:
        return str(result).strip()


#  Optional CLI test
if __name__ == "__main__":
    print("🧠 AI Lawyer - Legal Q&A Test")
    test_question = input("Enter your question: ")
    fake_case_text = "FIR mentions Section 420 and 406 IPC for cheating and breach of trust."
    response = answer_query(test_question, fake_case_text, llm_model)
    print("\n💬 AI Lawyer’s Answer:\n", response)
