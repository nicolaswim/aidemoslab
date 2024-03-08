
import numpy as np
def plot_spikey_circle_with_plotly(n):
    # Number of points to draw the circle
    points = 1000
    theta = np.linspace(0, 2*np.pi, points)
    
    # Base radius of the circle
    r_base = 1
    
    # Adjust these parameters to control the appearance of spikes
    alpha = 0.1 * n # Spike amplitude grows with n
    k = n # Spike frequency grows with n
    
    # Calculate the radius for each point
    r = r_base + alpha * np.sin(k * theta)
    
    # Convert polar coordinates to Cartesian coordinates for plotting
    x = r * np.cos(theta)
    y = r * np.sin(theta)
    
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=x, y=y, mode='lines'))
    fig.update_layout(title_text='Spikey Circle Plot', xaxis_title='X', yaxis_title='Y', xaxis=dict(scaleanchor="y", scaleratio=1))
    st.plotly_chart(fig, use_container_width=True)