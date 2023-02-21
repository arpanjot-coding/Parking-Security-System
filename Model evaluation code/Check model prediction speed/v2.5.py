import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_csv('output_data.csv')

# Create a line plot of the prediction times for all three models
fig, ax = plt.subplots()
for model_num in range(1, 4):
    model_col = f'Model{model_num} Prediction Time'
    ax.plot(df.index, df[model_col], label=f'Model {model_num}')
ax.set_xlabel('Frame Number')
ax.set_ylabel('Prediction Time (s)')
ax.legend()
plt.show()



# Create a line plot of the CPU usage for all three models
fig, ax = plt.subplots()
for model_num in range(1, 4):
    model_col = f'Model{model_num} CPU Usage'
    ax.plot(df.index, df[model_col], label=f'Model {model_num}')
ax.set_xlabel('Frame Number')
ax.set_ylabel('CPU Usage (%)')
ax.legend()
plt.show()

