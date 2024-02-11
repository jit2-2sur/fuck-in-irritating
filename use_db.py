"""other"""

import mychromadb
import chromadb
import re
from langchain_community.vectorstores import Chroma
from ai_models import embed_model, llm
import json

PERSIST_DIRECTORY = "./db"

'''
db = mychromadb.get_db(persist_dir=PERSIST_DIRECTORY)
docs = db.get()
print(docs)
print(db.get()["documents"][1])
'''

'''
persistent_client = chromadb.PersistentClient(path=PERSIST_DIRECTORY)
collection = persistent_client.get_collection("langchain")
#collection.add(ids=["1", "2", "3"], documents=["a", "b", "c"])

langchain_chroma = Chroma(
    client=persistent_client,
    collection_name="langchain",
    embedding_function=embed_model,
)

print("There are", langchain_chroma._collection.count(), "in the collection\n\n")

print(langchain_chroma.get()["documents"][1])
'''

#mychromadb.embed_document(file_path="./abc.pdf", file_name='abc.pdf')
#mychromadb.embed_document(persist_dir=PERSIST_DIRECTORY, file_path="./story1.pdf", collection_name="mysecondcollection")

db = mychromadb.get_db()
print(db._collection)
#docs = db.get(where={'source': updated_url})
#docs = db.get(where = {'source': 'D:\\fuck-in-irritating\\story1.pdf'})['documents']
#print(f"{docs}")

'''
print('\n\n\n\n\n')
db2 = mychromadb.get_db(persist_dir=PERSIST_DIRECTORY, collection_name="mysecondcollection")
#docs2 = db2.get()
#print((docs2))
print(db2._collection)
'''

#db.delete_collection()
#docs = db.get()
#print(docs)

docs = mychromadb.search_segment_in_db('moral of the story','story1.pdf')
print(docs)