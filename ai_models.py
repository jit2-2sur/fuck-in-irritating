"""storing all llm and embedding models"""

import os

from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_google_genai import GoogleGenerativeAI


api_key = os.environ.get("GOOGLE_API_KEY")  # provide your own palm api key

LLM_MODEL_NAME = "models/text-bison-001"
EMBED_MODEL_NAME = "sentence-transformers/all-mpnet-base-v2"
llm = GoogleGenerativeAI(model=LLM_MODEL_NAME, google_api_key=api_key)
embed_model = HuggingFaceEmbeddings(model_name=EMBED_MODEL_NAME)
