import pandas as pd
import numpy as np
import tkinter as tk
from tkinter import messagebox, filedialog
from openpyxl import Workbook

# Define the number of respondents and questions
NUM_QUESTIONS = 11
MAX_RESPONDENTS = 60

# Create the main application window
root = tk.Tk()
root.title("Likert Scale Survey Data Entry")
root.geometry("700x750")

# Frame to hold entries
frame = tk.Frame(root)
frame.pack()

# List to store respondent entries
entries = []

# Function to create entry fields for each question for each respondent
def create_entries():
    global entries
    entries.clear()  # Clear previous entries if re-running
    for i in range(MAX_RESPONDENTS):
        respondent_entries = []
        for j in range(NUM_QUESTIONS):
            entry = tk.Entry(frame, width=5)
            entry.grid(row=i + 1, column=j + 1, padx=2, pady=2)
            respondent_entries.append(entry)
        entries.append(respondent_entries)

# Function to calculate and save data
def calculate_and_save():
    # Collect data
    data = {f"Question {i+1}": [] for i in range(NUM_QUESTIONS)}
    
    for i in range(MAX_RESPONDENTS):
        for j in range(NUM_QUESTIONS):
            entry = entries[i][j]
            value = entry.get()
            if value:
                try:
                    value = int(value)
                    if value in [1, 2, 3, 4]:  # Ensure valid Likert scale value
                        data[f"Question {j+1}"].append(value)
                    else:
                        raise ValueError("Invalid entry")
                except ValueError:
                    messagebox.showerror("Input Error", f"Invalid entry in Respondent {i+1}, Question {j+1}")
                    return
            else:
                data[f"Question {j+1}"].append(np.nan)  # Treat empty cells as missing data
    
    # Convert data to DataFrame
    df = pd.DataFrame(data)
    
    # Calculate mean and standard deviation, skipping NaN values
    mean_values = df.mean()
    std_dev_values = df.std()
    
    # Append Mean and Standard Deviation to DataFrame
    df.loc['Mean'] = mean_values
    df.loc['Standard Deviation'] = std_dev_values
    
    # Ask user where to save the file
    file_path = filedialog.asksaveasfilename(defaultextension=".xlsx", filetypes=[("Excel files", "*.xlsx")])
    if file_path:
        # Save to Excel
        with pd.ExcelWriter(file_path, engine='openpyxl') as writer:
            df.to_excel(writer, sheet_name='Survey Analysis')
        messagebox.showinfo("Success", f"Data saved to '{file_path}'")

# Create header labels for questions
tk.Label(frame, text="Respondent").grid(row=0, column=0)
for j in range(NUM_QUESTIONS):
    label = tk.Label(frame, text=f"Q{j+1}")
    label.grid(row=0, column=j + 1)

# Create entry fields
create_entries()

# Button to calculate and save data
save_button = tk.Button(root, text="Calculate and Save", command=calculate_and_save)
save_button.pack(pady=10)

# Start the application
root.mainloop()
