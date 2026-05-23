from langchain_core.prompts import ChatPromptTemplate
from langchain_groq import ChatGroq

import uvicorn
from langserve import add_routes
from fastapi import FastAPI


#prompt1

e_prompt = ChatPromptTemplate.from_messages([
    ("system","Listen to user"),
    ("user","Give me an essay of 100 words on a topic{topic}")
])

#prompt2s

p_prompt = ChatPromptTemplate.from_template(
    """
       write a poem of 100 words where every word except the first word , start with the last letter of the previous word
       Give it on a topic{topic}    
    """
)

#llm

llm = ChatGroq(
    model = "llama-3.3-70b-versatile",
    api_key ="gsk_dwDmf0ARCXw....",
    temperature = 0
)

#app

app = FastAPI()

#essay route
add_routes(
    app,
    e_prompt | llm,
    path = "/essay"
)

#poem route
add_routes(
    app,
    p_prompt | llm,
    path = "/poem"
)


uvicorn.run(app, host = "Localhost", port=8000)

