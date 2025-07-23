import os
import json
import re
from dotenv import load_dotenv
from langdetect import detect
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS
from langchain.llms import CTransformers
from langchain.chains import RetrievalQA
from langchain.prompts import PromptTemplate
from huggingface_hub import login

# ----------------- Load environment variables and login -----------------
load_dotenv()
hf_api_key = os.getenv('HUGGINGFACEHUB_API_TOKEN')
login(token=hf_api_key)

# ----------------- Load and filter candidate data -----------------
with open('candidates.json', 'r') as f:
    data = json.load(f)

candidate_docs = []
for emp in data['employees']:
    # Filter out empty or incomplete records
    if (
        not emp.get('name') or
        not emp.get('skills') or
        not emp.get('projects') or
        emp.get('experience_years') is None
    ):
        continue

    doc = (
        f"{emp['name']} has {emp['experience_years']} years of experience. "
        f"Skills: {', '.join(emp['skills'])}. "
        f"Projects: {', '.join(emp['projects'])}. "
        f"Availability: {emp['availability']}."
    )
    candidate_docs.append(doc)

valid_candidate_count = len(candidate_docs)
print(f"[INFO] Valid candidates found: {valid_candidate_count}")

if valid_candidate_count == 0:
    raise ValueError("No valid candidate data available in the database.")

# ----------------- Create embeddings -----------------
text_splitter = RecursiveCharacterTextSplitter(chunk_size=512, chunk_overlap=50)
documents = text_splitter.create_documents(candidate_docs)

embeddings = HuggingFaceEmbeddings(model_name='sentence-transformers/all-MiniLM-L6-v2')
vector_db = FAISS.from_documents(documents, embeddings)

# ----------------- LLM with temperature control -----------------
llm = CTransformers(
    model="TheBloke/Mistral-7B-Instruct-v0.1-GGUF",
    model_type="mistral",
    temperature=0.2
)

# ----------------- Custom prompt -----------------
custom_prompt = PromptTemplate(
    input_variables=["context", "question"],
    template="""
You are an HR assistant. Based on the following context about available candidates, answer the user's request with a warm, structured, human-like recommendation listing the requested number of candidates with their details.

Context:
{context}

User Request:
{question}

Answer in this format:
"Based on your requirements for <requirements>, I found excellent candidates:
1) <Name>...
2) <Name>...
...
All have the technical depth and domain expertise you need. Would you like me to provide more details about their specific projects or check their availability for meetings?"
"""
)

# ----------------- Utility: Language detection -----------------
def is_supported_language(text):
    lang = detect(text)
    return lang == 'en'  # Extend if your model supports other languages

# ----------------- Utility: Extract requested number of candidates -----------------
def extract_requested_count(query):
    match = re.search(r'(\d+)\s*(candidate|person|people|profiles)?', query.lower())
    if match:
        n = int(match.group(1))
        # Limit to available candidates to avoid empty recommendations
        return min(max(n, 1), valid_candidate_count)
    # Default to 2, but cap to available
    return min(2, valid_candidate_count)

# ----------------- Main HR bot function -----------------
def ask_hr_bot(query):
    # Language check
    if not is_supported_language(query):
        return "Currently, this HR assistant supports English queries only. Please translate your request to English."

    # Basic relevance check
    if len(query.split()) < 3:
        return "Please provide a more detailed query to help me find the best candidates for you."

    relevant_keywords = ['find', 'suggest', 'developer', 'engineer', 'project', 'skills', 'experience', 'candidate', 'people', 'profiles']
    if not any(word in query.lower() for word in relevant_keywords):
        return "No matching candidates found for your request. Please provide a query related to candidate or project matching."

    # Determine number of candidates user requests
    num_candidates = extract_requested_count(query)

    retriever = vector_db.as_retriever(search_kwargs={"k": num_candidates})

    qa_chain = RetrievalQA.from_chain_type(
        llm=llm,
        retriever=retriever,
        chain_type_kwargs={"prompt": custom_prompt}
    )

    try:
        response = qa_chain.run(query)
    except Exception as e:
        print("[Error in qa_chain]", e)
        return "An error occurred while processing your request. Please try again."

    if not response.strip() or "I don't know" in response.lower():
        return "No matching candidates found for your request. Please refine your query with different skills, projects, or technologies."

    return response
