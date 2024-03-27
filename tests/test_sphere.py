import numpy as np
import matplotlib.pyplot as plt
from matplotlib.colors import LinearSegmentedColormap, Normalize
from matplotlib.cm import ScalarMappable
from mpl_toolkits.mplot3d import Axes3D  # This import registers the 3D projection

def plot_spikey_sphere_with_matplotlib(frequency, n):
    # Number of points to draw the circle/sphere
    points = 100
    phi = np.linspace(0, np.pi, points)  # From 0 to pi
    theta = np.linspace(0, 2*np.pi, points)  # From 0 to 2pi
    
    phi, theta = np.meshgrid(phi, theta)  # Create a meshgrid for spherical coordinates
    
    # Base radius of the sphere
    r_base = 1
    
    # Adjust these parameters to control the appearance of spikes
    alpha = 0.1 * n  # Spike amplitude grows with n
    k = n  # Spike frequency grows with n
    
    # Calculate the radius for each point with additional sinusoidal modulation
    r = r_base + alpha * np.sin(k * phi) + 0.1 * np.sin(frequency * theta)
    
    # Convert spherical coordinates to Cartesian coordinates for plotting
    x = r * np.sin(phi) * np.cos(theta)
    y = r * np.sin(phi) * np.sin(theta)
    z = r * np.cos(phi)
    
    # Custom colormap: green to blue to red
    cdict = {
        'red':   ((0.0, 0.0, 0.0), (0.5, 0.0, 0.0), (1.0, 1.0, 1.0)),
        'green': ((0.0, 1.0, 1.0), (0.5, 0.0, 0.0), (1.0, 0.0, 0.0)),
        'blue':  ((0.0, 0.0, 0.0), (0.5, 1.0, 1.0), (1.0, 0.0, 0.0))
    }
    custom_cmap = LinearSegmentedColormap('CustomCmap', segmentdata=cdict)
    
    # Set up the figure and axis for 3D plotting
    fig = plt.figure(figsize=(8, 6))
    ax = fig.add_subplot(111, projection='3d')

    # Plot the surface
    surf = ax.plot_surface(x, y, z, facecolors=plt.cm.viridis(r/np.max(r)))
    
    # Color scale from green (n=0) to blue to red (n=20)
    norm = Normalize(vmin=0, vmax=20)
    mappable = ScalarMappable(norm=norm, cmap=custom_cmap)
    mappable.set_array([])
    fig.colorbar(mappable, shrink=0.5, aspect=5, label='n value')
    
    ax.set_title(f'Spikey Sphere Plot - Frequency: {frequency}, n: {n}')
    ax.set_xlabel('X')
    ax.set_ylabel('Y')
    ax.set_zlabel('Z')
    
    # Show the plot
    plt.show()

# Example usage:
plot_spikey_sphere_with_matplotlib(10, 5)