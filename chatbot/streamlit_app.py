import streamlit as st
import redis
import time
import json
from datetime import datetime
import random

# Initialize Redis
r = redis.Redis()

# Setup Streamlit UI
st.title('Real-time Data Visualization')

# Placeholder for the plot
chart_placeholder = st.empty()

# Function to get data (simulate with Session State for example purposes)
def get_data():
    # Simulate retrieving the latest data point from Redis
    # In a real application, you'd subscribe to a channel and listen for new messages
    # This is a placeholder to simulate data updates
    data = st.session_state.get("data", [])
    return data

# Initial call to get_data to initialize the chart
data = get_data()
chart = st.line_chart(data)

# Main loop to update the chart
while True:
    # Simulate receiving a new data point
    new_point = {"time": datetime.now().strftime("%H:%M:%S"), "value": random.randint(0, 100)}
    data.append(new_point)
    st.session_state["data"] = data  # Update session state with new data

    # Update the chart
    chart.line_chart([point["value"] for point in data], use_container_width=True)
    
    # Simulate a delay to mimic real-time updates
    time.sleep(1)

    # Rerun the app to update the plot
    st.experimental_rerun()
