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
        user_input = st.text_input("You:", key='user_input', on_change=self.on_user_input_change)
        
        if st.session_state['last_response']:
            st.write(f"{st.session_state['last_response']}")

        with st.expander("Show Conversation History"):
            for interaction in st.session_state['memory']:
                st.text(f"User: {interaction['user']}")
                st.text(f"Bot: {interaction['bot']}")
                st.text("-----")

        # Calculate and display the total and current instance word counts
        total_word_count, current_instance_word_count = PostProcessing.calculate_word_count()
        if st.session_state['memory']:
            st.write(f"Total word count: {total_word_count} | Current instance word count: {current_instance_word_count}")
        else:
            st.write(f"Total word count: {total_word_count} | Current instance word count: 0")

        # Plot the spikey circle based on the current instance word count
        PostProcessing.plot_spikey_circle_based_on_word_count(current_instance_word_count)

        # Update and display the plot for word count
        PostProcessing.update_word_count_plot()

    def on_user_input_change(self):
        user_input = st.session_state['user_input']
        if user_input:  # Ensure there's input before proceeding
            self.chatbot.ask_chatbot(user_input)
            # After chatbot response, refresh the plots
            self.setup_ui()

# Initialize the chatbot
chatbot = ChatBot()

# Initialize and setup the Streamlit app UI
streamlit_app = StreamlitApp(chatbot)