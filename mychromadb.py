"""chromadb"""

from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.prompts import PromptTemplate
from langchain_community.document_loaders import PyPDFLoader
from langchain_community.vectorstores import Chroma
from langchain_core.output_parsers import StrOutputParser

from ai_models import embed_model, llm

# for storing chromadb embedded data in local machine
PERSIST_DIRECTORY = "./db"


def load_documents(file_path, file_name):
    """for loading files and splitting them into smaller chunks"""
    loader = PyPDFLoader(file_path)
    documents = loader.load()

    # adding pdf name to metadata for easy retrieval and accessibility
    for doc in documents:
        doc.metadata["file_name"] = file_name

    # splitting documents into smaller chunks if required, it automatically splits in pages
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=200)
    texts = text_splitter.split_documents(documents)

    return texts


def embed_document(file_path, file_name, collection_name="langchain"):
    """for embedding documents and storing data in vector database"""
    # getting the preprossed documents
    texts = load_documents(file_path, file_name)

    # embedding documents and storing in chromadb
    db = Chroma.from_documents(
        texts,
        embed_model,
        persist_directory=PERSIST_DIRECTORY,
        collection_name=collection_name,
    )

    return db


def get_db(collection_name="langchain"):
    """for getting database instance"""
    db = Chroma(
        persist_directory=PERSIST_DIRECTORY,
        embedding_function=embed_model,
        collection_name=collection_name,
    )

    return db


def search_segment_in_db(question, pdf_name):
    """for searching segments related to given question"""
    # connecting with vector database
    db = get_db()

    # searching in chromadb to retrieve segments related to question
    docs = db.similarity_search(question, filter={"file_name": pdf_name})

    return docs


def get_answer_from_palm(question, pdf_name):
    """for getting answer from palm llm models"""
    # searching in chromadb to retrieve segments related to question
    context = search_segment_in_db(question, pdf_name)

    # selecting only the most relevant segment
    context = context[0].page_content

    # prompt engineering through custom template
    template = """
    Context: {context}

    Question: {question}

    Answer:
    """

    # using langchain's PromptTemplate for creating prompt
    prompt = PromptTemplate.from_template(template)

    # using langchain's outputParser to get only answer content, removing metadata and other stuffs
    output_parser = StrOutputParser()

    # using langchain's chain to create a chain
    # that will concatenate the model with prompt and output parser
    chain = prompt | llm | output_parser

    # using langchain's invoke method to get answer
    answer = chain.invoke({"context": context, "question": question})

    return answer


def get_answer_from_palm2(question, pdf_name):
    """for getting answer from palm llm models"""
    # searching in chromadb to retrieve segments related to question
    context = search_segment_in_db(question, pdf_name)
    print(context)
    print(len(context))
    # selecting only the most relevant segment
    i = min(3, len(context))
    top_three_context = ""
    for j in range(i):
        top_three_context = top_three_context + context[j].page_content

    print(top_three_context)
    # prompt engineering through custom template
    template = """Context: {context}

Question: {question}

Answer:

give answer in full sentence
"""

    # using langchain's PromptTemplate for creating prompt
    prompt = PromptTemplate.from_template(template=template)
    print(prompt)

    # using langchain's outputParser to get only answer content, removing metadata and other stuffs
    output_parser = StrOutputParser()

    # using langchain's chain to create a chain
    # that will concatenate the model with prompt and output parser
    chain = prompt | llm | output_parser

    # using langchain's invoke method to get answer\
    try:
        answer = chain.invoke({"context": top_three_context, "question": question})
        response_data = {
            "message": "answer retrieved successfully",
            "question": question,
            "answer": answer,
        }
        return response_data
    except IndexError:
        response_data = {
            "message": "answer retrieval failed",
            "question": question,
            "answer": None,
        }
        return response_data
