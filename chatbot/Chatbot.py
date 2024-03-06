import streamlit as st
from langchain_openai import OpenAI
import openai
import os
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import plotly.graph_objects as go
import numpy as np


# Initialize your OpenAI API key
openai.api_key = os.getenv('OPENAI_API_KEY')

class ChatBot:
    def __init__(self):
        self.llm = OpenAI()
        self.initialize_memory()

    def initialize_memory(self):
        if 'memory' not in st.session_state:
            st.session_state['memory'] = []

    def add_interaction_to_memory(self, question, answer):
        st.session_state['memory'].append({'user': question, 'bot': answer})

    def get_formatted_memory(self):
        return "\n".join([f"User: {interaction['user']}\nBot: {interaction['bot']}" for interaction in st.session_state['memory']])

    def ask_chatbot(self, user_input):
        if user_input:
            formatted_memory = self.get_formatted_memory()
            prompt = f"{formatted_memory}\nUser: {user_input}\nBot:"
            response = self.llm.generate([prompt])
            bot_response = response.generations[0][0].text.strip()
            self.add_interaction_to_memory(user_input, bot_response)

            # Update the chat display
            st.session_state['last_response'] = bot_response
            st.session_state.user_input = ''  # Clear the input box after sending

