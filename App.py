import streamlit as st
from langchain_openai import OpenAI
import openai
import os
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import plotly.graph_objects as go
import numpy as np
from chatbot.Chatbot import ChatBot
from chatbot.PostProcessing import PostProcessing
import streamlit as st
from chatbot.Chatbot import ChatBot
from chatbot.PostProcessing import PostProcessing

class StreamlitApp:
    def __init__(self, chatbot):
        self.chatbot = chatbot
        self.initialize_session_state()
        self.setup_ui()

    def initialize_session_state(self):
        if 'user_input' not in st.session_state:
            st.session_state['user_input'] = ''
        if 'last_response' not in st.session_state:
            st.session_state['last_response'] = ''
        if 'memory' not in st.session_state:
            st.session_state['memory'] = []

    def setup_ui(self):
        st.title("Chatbot Conversation")
        
        col1, col2 = st.columns([3, 1])  # Adjusting the column width ratio for better layout

        with col1:  # Chat and history UI
            user_input = st.text_input("You:", key='user_input', on_change=self.on_user_input_change)
            if st.session_state['last_response']:
                st.write(f"{st.session_state['last_response']}")

            with st.expander("Show Conversation History"):
                for interaction in st.session_state['memory']:
                    st.text(f"User: {interaction['user']}")
                    st.text(f"Bot: {interaction['bot']}")
                    st.text("-----")

        with col2:  # Only water usage metric and image
            total_water_usage_ml, deviation_water_usage_ml = PostProcessing.calculate_water_usage_deviation()
            st.metric(label="Water Usage (ml)", value=f"{total_water_usage_ml}", delta=f"{deviation_water_usage_ml}")
            PostProcessing.display_interaction_image()  # Displays the bottle image based on the interaction count

        self.display_markdown_dropdown()

    def display_markdown_dropdown(self):
        # Load Markdown text from file
        with open('waterinfo/waterinfo.md', 'r') as file:
            markdown_text = file.read()
        
        # Expander to toggle Markdown display
        with st.expander("Show Additional Information"):
            st.markdown(markdown_text, unsafe_allow_html=True)
    
    def on_user_input_change(self):
        user_input = st.session_state['user_input']
        if user_input:  # Ensure there's input before proceeding
            self.chatbot.ask_chatbot(user_input)
            # After chatbot response, refresh the UI
            self.setup_ui()

# Initialize the chatbot
chatbot = ChatBot()

# Initialize and setup the Streamlit app UI
streamlit_app = StreamlitApp(chatbot)
