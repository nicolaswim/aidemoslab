import numpy as np
import matplotlib.pyplot as plt

def custom_function(x):
    if x <= 200:
        # Linear increase for the first 200 entries
        return x
    else:
        # After 200, it marginally increases
        # Adjust the rate of increase as needed
        return 200 + (np.log(x - 199) * 10)

# Generating values for demonstration
x_values = np.arange(0, 300)
y_values = np.array([custom_function(x) for x in x_values])

# Plotting
plt.figure(figsize=(10, 6))
plt.plot(x_values, y_values, label="Custom Function")
plt.xlabel('X')
plt.ylabel('Value')
plt.title('Custom Function Behavior')
plt.legend()
plt.grid(True)
plt.show()
