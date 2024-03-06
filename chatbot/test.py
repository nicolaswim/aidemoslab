import numpy as np
import matplotlib.pyplot as plt

def draw_spikey_circle(n):
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
    
    plt.figure(figsize=(6,6))
    plt.plot(x, y)
    plt.axis('equal') # Ensure the x and y axes have the same scale
    plt.show()

# Example usage
draw_spikey_circle(40) # Change the input here to see different shapes
