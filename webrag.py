from langchain_community.document_loaders import WebBaseLoader
import bs4

# obj = classname()

loader = WebBaseLoader(
    "https://www.apple.in"

   )


docs = loader.load()

from langchain.text_splitter import RecursiveCharacterTextSplitter

splitter = RecursiveCharacterTextSplitter(chunk_size=1000,chunk_overlap=200)
document = splitter.split_documents(docs)
#print(document[:10])

from langchain_community.embeddings import OllamaEmbeddings

from langchain_milvus import Milvus

#embeddings
embed = OllamaEmbeddings(model="llama2")

#uri setup
#URI = "C:\Users\VENU\Desktop\check.db"
URI = "/check.db"

vdb = Milvus (
    embedding_function = embed,
    connection_args = {"uri": URI},

)

from uuid import uuid4
uuids = [str(uuid4()) for _ in range(len(document))] #list comprehension

vdb.add_documents(documents=document, ids = uuids)

from langchain_core.prompts import ChatPromptTemplate
from langchain_community.llms import ollama
from langchain_core.output_parsers import StrOutputParser


ret = vdb.as_retriever()

prompt = ChatPromptTemplate.from_template(

    """
    Answer the question based only on the following context:
    {context}
    Question : {question}

    """
)

from langchain_community.llms import ollama

model = ollama(model="llama2")
oparser = StrOutputParser()

from langchain_core.runnables import RunnablePassthrough

chain = (

    {"context":ret, "question":RunnablePassthrough()}
    |prompt|model|oparser

)

import streamlit as st

st.title("Apple RAG")

input_text = st.text_input("Enter the question related only to APPLE")

st.write(chain.invoke({"question":input_text}))


