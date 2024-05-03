import streamlit as st
from langchain_openai import OpenAI
import openai
import os
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import plotly.graph_objects as go
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.colors import LinearSegmentedColormap, Normalize
from matplotlib.cm import ScalarMappable

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
        points = 1000
        theta = np.linspace(0, 2 * np.pi, points)
        r_base = 1
        alpha = 0.1 * n
        k = n
        r = r_base + alpha * np.sin(k * theta) + 0.1 * np.sin(frequency * theta)

        x = r * np.cos(theta)
        y = r * np.sin(theta)

        cdict = {
            'red':   ((0.0, 0.0, 0.0), (0.5, 0.0, 0.0), (1.0, 1.0, 1.0)),
            'green': ((0.0, 1.0, 1.0), (0.5, 0.0, 0.0), (1.0, 0.0, 0.0)),
            'blue':  ((0.0, 0.0, 0.0), (0.5, 1.0, 1.0), (1.0, 0.0, 0.0))
        }
        custom_cmap = LinearSegmentedColormap('CustomCmap', segmentdata=cdict)
        
        # Color scale from green (n=0) to blue to red (n=20)
        norm = Normalize(vmin=0, vmax=20)
        mappable = ScalarMappable(norm=norm, cmap=custom_cmap)
        color = mappable.to_rgba(n)
        color = 'rgba({}, {}, {}, {})'.format(int(color[0]*255), int(color[1]*255), int(color[2]*255), color[3])

        fig = go.Figure()
        fig.add_trace(go.Scatter(x=x, y=y, mode='lines', name='Spikey Circle',
                                 line=dict(color=color)))

        fig.update_layout(title=f'Visual chat interpretation - Frequency: {frequency}, n: {n}',
                          xaxis_title='X', yaxis_title='Y',
                          xaxis=dict(scaleanchor="y", scaleratio=1), yaxis=dict(autorange=True))

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

    @staticmethod
    def calculate_co2_emissions_deviation():
        number_of_interactions = len(st.session_state['memory'])
        current_co2_emissions = number_of_interactions * 4.32
        previous_co2_emissions = (number_of_interactions - 1) * 4.32 if number_of_interactions > 0 else 0
        deviation_co2_emissions = current_co2_emissions - previous_co2_emissions
        return current_co2_emissions, deviation_co2_emissions

    @staticmethod
    def calculate_water_usage_deviation():
        number_of_questions = len(st.session_state['memory'])
        current_water_usage_ml = (number_of_questions / 20) * 500
        previous_questions = number_of_questions - 1
        previous_water_usage_ml = (previous_questions / 20) * 500 if previous_questions > 0 else 0
        deviation_water_usage_ml = current_water_usage_ml - previous_water_usage_ml
        return current_water_usage_ml, deviation_water_usage_ml
    
    # @staticmethod
    # def display_interaction_image():
    #     interaction_count = len(st.session_state['memory']) + 1  # +1 to match question count including current
    #     if interaction_count < 11:
    #         image_path = f'images/river/{interaction_count}.png'
            
    #     else:
    #         image_path = 'images/river/11.png'
        
    #     if os.path.exists(image_path):
    #         st.image(image_path, caption='River View', use_column_width=True)
    #     else:
    #         st.write("Image not found.")
    @staticmethod
    def display_interaction_image():
        interaction_count = len(st.session_state['memory']) + 1  # +1 to match question count including current
        # Use interaction count directly to select the next image, cycling from 1 to 20
        image_index = (interaction_count - 1) % 20 + 1  # Calculate the next image index
        image_path = f'images/bottle/water_bottle-{image_index:02}.png'
        
        if os.path.exists(image_path):
            st.image(image_path, caption=f'Water Usage', use_column_width=True)
        else:
            st.write("Image not found.")



    



