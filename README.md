# HR-Resource_Query_Chatbot-

# HR Query Chatbot using LangChain, FAISS, and LLM

## Project Overview

This project is an HR Resource Query Chatbot that:
- Allows users (HR teams) to query for candidates based on skills, experience, and project details.
- Fetches candidate data from a structured JSON database.
- Uses LangChain + FAISS for retrieval and LLM for generation to provide human-like, structured candidate recommendations.
- Supports both:
  - Streamlit UI for easy interaction.
  - FastAPI endpoints for programmatic management of the candidate database.

## Features

- Query candidates by skills, projects, and experience (e.g., "Find Python developers with 3+ years experience.")
- Retrieves and filters candidates intelligently from your database.
- Uses HuggingFaceEmbeddings via LangChain for embeddings.
- Uses Mistral LLM via LangChain for structured, warm responses.
- User-friendly Streamlit interface for HR teams.
- FastAPI for managing candidate data (GET, POST, PUT).
- Language detection (English-only support currently).
- Environment variable management with .env for Hugging Face API integration.

## Repository Structure

.
├── app.py                  # Streamlit front-end for HR Bot
├── hr_bot.py               # Core HR Bot logic (retrieval + LLM generation)
├── data_base_api.py        # FastAPI endpoints for candidate management
├── candidates.json         # Candidate database (JSON)
├── .env                    # Environment variables (Hugging Face API key)
├── req.txt        # Python dependencies
└── README.md               # Project documentation

## Requirements

- Python 3.10+
- Hugging Face account with API token
- Virtual environment recommended for isolation.

## Installation

1. Clone the repository:
git clone https://github.com/Surajvijendra/HR-Resource_Query_Chatbot-.git
cd hr-query-chatbot

2. Create a virtual environment:
conda create -p hr_env python=3.10
conda activate hr_env/         # On Windows

3. Install dependencies:
pip install -r req.txt

4. Set up environment variables:
Create a .env file with:
HUGGINGFACEHUB_API_TOKEN=your_hf_token_here

5. Ensure candidates.json exists:
The bot uses this file as its database for candidate retrieval. Ensure it is structured as:
{
  "employees": [
    {
      "id": 1,
      "name": "Alice",
      "skills": ["Python", "FastAPI"],
      "experience_years": 3,
      "projects": ["E-commerce platform"],
      "availability": "Immediate"
    }
  ]
}

## Running the Applications

### 1. Run the Streamlit HR Query Chatbot

streamlit run app.py

- Open the provided local URL to interact with the HR Bot.
- Enter queries like:
  - "Find Python developers with 3+ years experience."
  - "Suggest 2 data scientists with NLP experience."

### 2. Run the FastAPI Candidate Database API

uvicorn data_base_api:app --reload

Available endpoints:

- GET /candidates – List all candidates.
- POST /candidates – Add a new candidate.
- PUT /candidates/{candidate_id} – Update candidate details.

Use Swagger UI at:
http://127.0.0.1:8000/docs
for interactive API testing.

## How It Works

1. Candidate Data:
Stored in candidates.json, containing details like name, skills, projects, experience, and availability.

2. Embeddings:
Uses HuggingFaceEmbeddings via LangChain for embeddings, to embed candidate details and store in FAISS for efficient retrieval.

3. LLM for Structured Responses:
Uses Mistral 7B (TheBloke/Mistral-7B-Instruct-v0.1-GGUF) to generate human-like recommendations based on user queries.

4. Query Flow:
- User asks a question (via Streamlit or API).
- Bot detects the language and validates the query.
- Retrieves relevant candidates from the FAISS vector store.
- Passes context and user query to the LLM.
- Returns a clean, structured, warm HR recommendation.

## Example Usage

User Query:
"Find 3 Python developers with FastAPI and ML experience."

Bot Response:
"Based on your requirements for Python, FastAPI, and ML, I found excellent candidates:
1) Rahul – 4 years experience...
2) Naveen – 3 years experience...
3) charan – 5 years experience...
All have the technical depth and domain expertise you need. Would you like me to provide more details about their specific projects or check their availability for meetings?"

## Contributing

If you wish to improve features (e.g., multilingual support, advanced ranking, admin dashboard), feel free to open a PR or issue.


## Acknowledgements

- LangChain
- FAISS
- Hugging Face
- Streamlit
- FastAPI
