#gsk_dwDmf0A....

#streamlit
import streamlit as st

#
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

#groq
from langchain_groq import ChatGroq

#creating prompts

prompt = ChatPromptTemplate.from_template (
    """
    I want you to give me exact answer about question {question}

    """
)

#llm 

llm = ChatGroq (
    model = "llama-3.3-70b-versatile",
    api_key ="gsk_dwDmf0A....",
    temperature = 0
)


#outputparser

op= StrOutputParser()

#chain

chain = prompt |llm| op

#website
st.title("Venu's Robot")
input_text = st.text_input("Enter your prompt... ")
response = chain.invoke({"question":input_text})
st.write(response)