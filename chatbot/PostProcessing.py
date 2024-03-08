import streamlit as st
from langchain_openai import OpenAI
import openai
import os
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import plotly.graph_objects as go
import numpy as np
# from Chatbot import ChatBot

class PostProcessing:
    @staticmethod
    def calculate_word_count():
        if st.session_state['memory']:
            current_instance_word_count = len(st.session_state['memory'][-1]['user'].split()) + len(st.session_state['memory'][-1]['bot'].split())
        else:
            current_instance_word_count = 0
        total_word_count = sum(len(interaction['user'].split()) + len(interaction['bot'].split()) for interaction in st.session_state['memory'])
        return total_word_count, current_instance_word_count

    @staticmethod
    def update_word_count_plot():
        word_counts_per_instance = [len(interaction['user'].split()) + len(interaction['bot'].split()) for interaction in st.session_state['memory']]
        cumulative_word_counts = [sum(word_counts_per_instance[:i+1]) for i in range(len(word_counts_per_instance))]
        instances = list(range(1, len(word_counts_per_instance) + 1))

        fig = go.Figure(data=[go.Scatter3d(
            x=instances,
            y=cumulative_word_counts,
            z=word_counts_per_instance,
            mode='markers+lines',
            marker=dict(
                size=5,
                opacity=0.8,
            ),
        )])

        fig.update_layout(
            title='3D Plot of Word Counts',
            scene=dict(
                xaxis_title='Instance Number',
                yaxis_title='Total Word Count',
                zaxis_title='Word Count Per Instance'
            ),
            margin=dict(l=0, r=0, b=0, t=0)
        )

        st.plotly_chart(fig, use_container_width=True)

    # @staticmethod
    # def plot_spikey_circle_with_plotly(n):
    #     # Number of points to draw the sphere
    #     points = 1000
    #     phi = np.linspace(0, np.pi, points)  # Azimuthal angle
    #     theta = np.linspace(0, 2*np.pi, points)  # Polar angle
        
    #     # Base radius of the sphere
    #     r_base = 1
        
    #     # Adjust these parameters to control the appearance of spikes
    #     alpha = 0.1 * n  # Spike amplitude grows with n
    #     k = n  # Spike frequency grows with n
        
    #     # Calculate the radius for each point
    #     r = r_base + alpha * np.sin(k * phi)
        
    #     # Convert spherical coordinates to Cartesian coordinates for plotting
    #     x = r * np.outer(np.sin(phi), np.cos(theta))
    #     y = r * np.outer(np.sin(phi), np.sin(theta))
    #     z = r * np.outer(np.cos(phi), np.ones_like(theta))
        
    #     fig = go.Figure()
    #     fig.add_trace(go.Surface(x=x, y=y, z=z))
    #     fig.update_layout(title_text='Spikey Sphere Plot (3D)', scene=dict(xaxis_title='X', yaxis_title='Y', zaxis_title='Z'))
    #     st.plotly_chart(fig, use_container_width=True)

    @staticmethod
    def plot_spikey_circle_with_plotly(frequency, n):
        # Number of points to draw the circle
        points = 1000
        theta = np.linspace(0, 2 * np.pi, points)

        # Base radius of the circle
        r_base = 1

        # Adjust these parameters to control the appearance of spikes
        alpha = 0.1 * n  # Spike amplitude grows with n
        k = n  # Spike frequency grows with n

        # Calculate the radius for each point with additional sinusoidal modulation
        r = r_base + alpha * np.sin(k * theta) + 0.1 * np.sin(frequency * theta)

        # Convert polar coordinates to Cartesian coordinates for plotting
        x = r * np.cos(theta)
        y = r * np.sin(theta)

        # Map n to a color in the Viridis colorscale
        colorscale = 'Viridis'  # Feel free to change this to any Plotly colorscale
        # Normalize n to a 0-1 range based on your expected n min/max values for the colorscale
        n_normalized = n / 20 if n <= 20 else 1  # Assuming n ranges from 0 to 20

        # Create the plot with Plotly
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=x, y=y, mode='lines', name='Spikey Circle',
                                line=dict(color=f'rgba({n_normalized}, {n_normalized}, {n_normalized})')))
        fig.update_layout(title=f'Spikey Circle Plot - Frequency: {frequency}, n: {n}',
                        xaxis_title='X',
                        yaxis_title='Y',
                        xaxis=dict(scaleanchor="y", scaleratio=1),
                        yaxis=dict(autorange=True))
        # Create the plot with Plotly
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=x, y=y, mode='lines', name='Spikey Circle',
                                line=dict(color=f'rgba({n_normalized}, {n_normalized}, {n_normalized})')))
        fig.update_layout(title=f'Spikey Circle Plot - Frequency: {frequency}, n: {n}',
                        xaxis_title='X',
                        yaxis_title='Y',
                        xaxis=dict(scaleanchor="y", scaleratio=1),
                        yaxis=dict(autorange=True))
        st.plotly_chart(fig, use_container_width=True)
    
    @staticmethod
    def custom_function(x):
        var = 10
        x = x/50
        if x <= var:
            return x
        else:
            return var + (np.log(x-var-1) * 10)
    
    @staticmethod
    def plot_spikey_circle_based_on_word_count(current_instance_word_count, total_word_count):
        tot = PostProcessing.custom_function(total_word_count)
        PostProcessing.plot_spikey_circle_with_plotly(current_instance_word_count, tot)
    



