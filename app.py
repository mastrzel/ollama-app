import streamlit as st
import time
from langchain_core.prompts import ChatPromptTemplate
from langchain_ollama.llms import OllamaLLM
from langchain_core.output_parsers import StrOutputParser

OLLAMA_MODEL = "SpeakLeash/bielik-7b-instruct-v0.1-gguf"
PROMPT_TEMPLATE = """Odpowiedz na pytanie: {question}"""
CHAT_TITLE = "Ollama chat"
CHAT_HINT = "Co tam?"

# Streamed response emulator
def response_generator(user_input):
    prompt = ChatPromptTemplate.from_template(PROMPT_TEMPLATE)

    model = OllamaLLM(model=OLLAMA_MODEL)

    chain = prompt | model | StrOutputParser()

    response = chain.invoke({"question": user_input})

    for word in response.split():
        yield word + " "
        time.sleep(0.05)


st.title(CHAT_TITLE)

# Accept user input
if user_input := st.chat_input(CHAT_HINT):
    # Display user message in chat message container
    with st.chat_message("user"):
        st.markdown(user_input)

    # Display assistant response in chat message container
    with st.chat_message("assistant"):
        response = st.write_stream(response_generator(user_input))