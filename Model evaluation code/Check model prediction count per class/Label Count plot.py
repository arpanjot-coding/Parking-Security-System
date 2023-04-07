import pandas as pd
import matplotlib.pyplot as plt

# Read the CSV file into a pandas dataframe
df = pd.read_csv('output_data.csv')

# Convert the string data for both models to dictionaries
model1_data = df['model1'].apply(eval)
coco_data = df['coco'].apply(eval)

# Loop over each class
for class_name in ['Car door close', 'Car door open', 'parking', 'number plate']:

    # Create an empty dictionary to hold the counts for the class
    counts = {
        'model1': [],
        'coco': []
    }

    # Loop over each row in the dataframe and count the occurrences of the class
    for index, row in df.iterrows():
        model1_counts = eval(row['model1'])
        coco_counts = eval(row['coco'])
        counts['model1'].append(model1_counts.get(class_name, 0))
        counts['coco'].append(coco_counts.get(class_name, 0))

    # Create a pandas dataframe from the counts dictionary
    data = pd.DataFrame(counts)

    # Plot the data for the class
    plt.plot(data.index, data['model1'], label='model1')
    plt.plot(data.index, data['coco'], label='coco')

    # Add axis labels and a title
    plt.xlabel('Frame count')
    plt.ylabel('Count')
    plt.title(class_name)

    # Add a legend
    plt.legend()

    # Show the plot
    plt.show()
