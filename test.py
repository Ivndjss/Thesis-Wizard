import pandas as pd
import numpy as np

# Sample data for demonstration
data = {
    'Question 1': [4, 3, 2, 4, 3, 4],
    'Question 2': [3, 2, 1, 2, 2, 3],
    'Question 3': [4, 4, 3, 3, 3, 4]
}

# Convert the data into a DataFrame
df = pd.DataFrame(data)

# Calculate the mean and standard deviation for each question
mean_values = df.mean()
std_dev_values = df.std()

# Append Mean and Std Dev rows
df.loc['Mean'] = mean_values
df.loc['Standard Deviation'] = std_dev_values

# Save the data to an Excel file in the specified folder
output_file = r"C:\Users\Arcly-za B Aguinaldo\Desktop\Python\Likert_Scale_Analysis.xlsx"
with pd.ExcelWriter(output_file, engine='openpyxl') as writer:
    df.to_excel(writer, sheet_name='Survey Analysis')

print(f"Excel file saved as '{output_file}' with the calculated mean and standard deviation.")
