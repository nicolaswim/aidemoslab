# %matplotlib notebook
import matplotlib.pyplot as plt
import numpy as np
import time

# Initialize plot
plt.ion()  # Turn on interactive mode
fig, ax = plt.subplots()
x, y = [], []
sc = ax.scatter(x, y)
plt.ylabel('Word Count')
plt.xlabel('Message Number')

def update_plot(new_y):
    x.append(len(x))  # Increment x based on the number of entries
    y.append(new_y)
    sc.set_offsets(np.c_[x,y])
    ax.relim()
    ax.autoscale_view()
    fig.canvas.draw_idle()
    fig.canvas.flush_events()

# Example of updating the plot with new data
for i in range(10000):  # Simulate incoming messages
    update_plot(np.random.randint(10, 50))  # Random word count
    time.sleep(1)  # Wait a bit before the next update
