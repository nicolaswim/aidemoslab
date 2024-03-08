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
        
        col1, col2 = st.columns([1, 1])  # Equal space for both columns

        with col1:  # Chat and history UI
            user_input = st.text_input("You:", key='user_input', on_change=self.on_user_input_change)
            if st.session_state['last_response']:
                st.write(f"{st.session_state['last_response']}")

            with st.expander("Show Conversation History"):
                for interaction in st.session_state['memory']:
                    st.text(f"User: {interaction['user']}")
                    st.text(f"Bot: {interaction['bot']}")
                    st.text("-----")

        with col2:  # Metrics UI
            total_word_count, current_instance_word_count = PostProcessing.calculate_word_count()
            deviation_word_count = current_instance_word_count - (len(st.session_state['memory'][-2]['user'].split()) + len(st.session_state['memory'][-2]['bot'].split())) if len(st.session_state['memory']) >= 2 else current_instance_word_count
            
            total_co2_emissions, deviation_co2_emissions = PostProcessing.calculate_co2_emissions_deviation()
            total_water_usage_ml, deviation_water_usage_ml = PostProcessing.calculate_water_usage_deviation()

            metric_col1, metric_col2 = st.columns(2)
            with metric_col1:
                st.metric(label="Total Words", value=total_word_count, delta=current_instance_word_count, delta_color="inverse")
                st.metric(label="CO2 Emissions (units)", value=f"{total_co2_emissions:.2f}", delta=f"{deviation_co2_emissions:.2f}")
            with metric_col2:
                st.metric(label="Current Interaction Words", value=current_instance_word_count, delta=deviation_word_count, delta_color="normal")
                st.metric(label="Water Usage (ml)", value=f"{total_water_usage_ml}", delta=f"{deviation_water_usage_ml}")
            
        PostProcessing.plot_spikey_circle_based_on_word_count(current_instance_word_count, total_word_count)


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
