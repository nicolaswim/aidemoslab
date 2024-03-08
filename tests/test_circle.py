import numpy as np
import matplotlib.pyplot as plt
from matplotlib.colors import LinearSegmentedColormap, Normalize
from matplotlib.cm import ScalarMappable

def plot_spikey_circle_with_matplotlib(frequency, n):
    # Number of points to draw the circle
    points = 1000
    theta = np.linspace(0, 2*np.pi, points)
    
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
    
    # Custom colormap: green to blue to red
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
    
    # Create the plot
    plt.figure(figsize=(6,6))
    plt.plot(x, y, color=color)
    plt.title(f'Spikey Circle Plot - Frequency: {frequency}, n: {n}')
    plt.xlabel('X')
    plt.ylabel('Y')
    plt.axis('equal')  # Equal scaling for both axes
    plt.colorbar(mappable, label='n value', extend='both')
    
    # Display the plot
    plt.show()

# Example usage:
plot_spikey_circle_with_matplotlib(30, 20.4)
