"""chromadb"""

import textwrap

from langchain.chains import RetrievalQA
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import PyPDFLoader
from langchain_community.vectorstores import Chroma

from ai_models import embed_model, llm

PERSIST_DIRECTORY = "./db"

'''
def wrap_text_preserve_newlines(text, width=110):
    """for preserving new lines in text"""
    # Split the input text into lines based on newline characters
    lines = text.split("\n")

    # Wrap each line individually
    wrapped_lines = [textwrap.fill(line, width=width) for line in lines]

    # Join the wrapped lines back together using newline characters
    wrapped_text = "\n".join(wrapped_lines)

    return wrapped_text


def process_llm_response(llm_response):
    """for processing llm response so that it look more presentable"""
    print(wrap_text_preserve_newlines(llm_response["result"]))
    print("\n\nSources:")
    for source in llm_response["source_documents"]:
        print(source.metadata["source"])
'''

def load_documents(file_path, file_name):
    """for loading files and splitting them into smaller chunks"""
    loader = PyPDFLoader(file_path)
    documents = loader.load()
    for doc in documents:
        doc.metadata["file_name"] = file_name

    text_splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=200)
    texts = text_splitter.split_documents(documents)

    return texts


def embed_document(file_path, file_name, collection_name="langchain"):
    """for embedding documents and storing data in vector database"""
    texts = load_documents(file_path, file_name)
    db = Chroma.from_documents(
        texts,
        embed_model,
        persist_directory=PERSIST_DIRECTORY,
        collection_name=collection_name,
    )

    return db


def get_db(collection_name="langchain"):
    """for getting database"""
    db = Chroma(
        persist_directory=PERSIST_DIRECTORY,
        embedding_function=embed_model,
        collection_name=collection_name,
    )

    return db

def search_segment_in_db(question, pdf_name):
    """for searching segments related to given question"""
    db = get_db()
    docs = db.similarity_search(question, filter= {'file_name': pdf_name})
    return docs


def get_answer_from_palm(question, pdf_name):
    """for getting answer from palm llm models"""
    context = search_segment_in_db(question, pdf_name)
    answer = llm.invoke(question, context)
    return answer


def retrieve_data(db):
    """for retrieving data"""
    retriever = db.as_retriever()
    qa_chain = RetrievalQA.from_chain_type(
        llm=llm, chain_type="stuff", retriever=retriever, return_source_documents=True
    )
