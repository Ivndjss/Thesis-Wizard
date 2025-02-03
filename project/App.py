import os
from flask import Flask, render_template, request, redirect, url_for, flash
import pandas as pd
import numpy as np
from openpyxl import Workbook

app = Flask(__name__)
app.secret_key = 'Y0uR$3cRE7k3Y'  # Replace with a strong secret key

# Define the questionnaire structure (IT Experts)
questions = [
    "Precision: The system accurately identifies characters in handwritten text without confusion.",
    "Precision: The application demonstrates high precision in recognizing similar characters with minimal errors.",
    "Precision: Precision in text recognition remains consistent across various handwriting styles.",
    "Precision: The system’s output accurately represents the intended handwritten input.",
    "Precision: Handwritten character misrecognition is minimal within the application's results.",
    "Precision: The system maintains high precision even with variations in handwriting pressure or slant.",
    "Recall: The system successfully retrieves all necessary characters from handwritten input.",
    "Recall: The application minimizes the omission of characters during text recognition.",
    "Recall: Recall accuracy is maintained even when handwriting is complex or non-standard.",
    "Recall: The system reliably captures the complete content of handwritten text.",
    "Recall: Recognition of characters is thorough, covering all portions of handwritten entries.",
    "Recall: Handwritten text is fully represented in digital conversion without loss of characters.",
    "F-Measure: The balance between precision and recall is well-managed in the system’s output.",
    "F-Measure: The application demonstrates reliable F-measure scores in varied test scenarios.",
    "F-Measure: The system’s F-measure metric reflects accurate and thorough recognition results.",
    "F-Measure: The application’s performance on F-measure remains stable across different handwriting styles.",
    "F-Measure: F-measure values indicate that the system maintains effectiveness in recognizing handwritten input.",
    "F-Measure: Performance in achieving a balanced F-measure is consistent with high-accuracy standards.", 
    "Word Error Rate(WER): The system exhibits a low Character Error Rate in recognizing individual handwritten characters.",
    "Word Error Rate(WER): CER values indicate that the system performs well with minimal character-level inaccuracies.",
    "Word Error Rate(WER): Character recognition remains accurate regardless of variations in character shapes.",
    "Word Error Rate(WER): The application reliably minimizes character recognition errors during the conversion process.",
    "Word Error Rate(WER): The system shows consistent character accuracy across different samples of handwriting.",
    "Word Error Rate(WER): CER metrics align with expectations for accurate character-level recognition.",
    "Character Error Rate(CER): The application maintains a low Word Error Rate during the recognition process.",
    "Character Error Rate(CER): WER scores suggest that the system effectively recognizes entire words in handwritten input.",
    "Character Error Rate(CER): Word recognition is accurate, minimizing the chance of misinterpretation of handwritten words.",
    "Character Error Rate(CER): The system exhibits reliability in recognizing words across varied handwriting styles.",
    "Character Error Rate(CER): Word Error Rates remain low, even when processing complex or joined-up handwriting.",
    "Character Error Rate(CER): WER performance meets expected standards for accurate word-level recognition.",
]

# Define the questionnaire structure (Normal Users)
# questions = [
#     "Precision: The app correctly recognizes characters in handwritten text.",
#     "Precision: The app rarely makes mistakes with characters that look similar.",
#     "Precision: It works well with different handwriting styles.",
#     "Precision: The text shown on screen matches what was written by hand.",
#     "Precision: There are very few mistakes when recognizing handwritten characters.",
#     "Precision: The app keeps accuracy even with changes in handwriting pressure or slant.",
#     "Recall: The app finds and recognizes all characters from handwritten text.",
#     "Recall: It does not miss any characters when reading handwriting.",
#     "Recall: It can read complex or unique handwriting accurately.",
#     "Recall: The app captures the full handwritten text without leaving anything out.",
#     "Recall: Every part of the handwriting is included in the digital version.",
#     "Recall: There’s no missing information in the digital text conversion.",
#     "F-Measure: The app balances accuracy and completeness well.",
#     "F-Measure: It performs consistently across different handwriting tests.",
#     "F-Measure: The app reliably recognizes handwritten text in a balanced way.",
#     "F-Measure: Its performance stays high with different handwriting styles.",
#     "F-Measure: It keeps a good balance between accuracy and completeness.",
#     "F-Measure: The app consistently performs well in recognizing handwriting.",
#     "Character Error Rate (CER): The app has very few mistakes in individual character recognition.",
#     "Character Error Rate (CER): Mistakes at the character level are minimal.",
#     "Character Error Rate (CER): It accurately recognizes characters even if shapes vary.",
#     "Character Error Rate (CER): The app reliably keeps character mistakes low during conversion.",
#     "Character Error Rate (CER): It performs well with different samples of handwriting.",
#     "Character Error Rate (CER): Character accuracy meets expectations.",
#     "Word Error Rate (WER): The app keeps mistakes low when recognizing whole words.",
#     "Word Error Rate (WER): It effectively recognizes full words from handwritten text.",
#     "Word Error Rate (WER): It rarely misinterprets handwritten words.",
#     "Word Error Rate (WER): The app reliably reads words across different handwriting styles.",
#     "Word Error Rate (WER): Word mistakes remain low even with complex handwriting.",
#     "Word Error Rate (WER): Word accuracy meets expected standards.",
# ]

@app.route('/')
def index():
    return render_template('index.html', questions=questions)

@app.route('/submit', methods=['POST'])
def submit():
    # Collect data
    respondents_data = []
    num_respondents = int(request.form.get("num_respondents", 0))

    for i in range(num_respondents):
        respondent_data = {}
        for j, question in enumerate(questions):
            value = request.form.get(f'respondent{i}_question{j}')
            if value:
                try:
                    value = int(value)
                    if value in [1, 2, 3, 4]:  # Ensure valid Likert scale value
                        respondent_data[f"Question {j+1}"] = value
                    else:
                        flash(f"Invalid entry for Respondent {i+1}, Question {j+1}")
                        return redirect(url_for('index'))
                except ValueError:
                    flash(f"Invalid entry for Respondent {i+1}, Question {j+1}")
                    return redirect(url_for('index'))
            else:
                respondent_data[f"Question {j+1}"] = np.nan  # Missing data
        respondents_data.append(respondent_data)

    # Convert data to DataFrame
    df = pd.DataFrame(respondents_data)

    # Calculate mean, median, and weighted mean, skipping NaN values
    mean_values = df.mean()
    median_values = df.median()
    
    # Calculate weighted mean for each question (assuming equal weights of 1, 2, 3, and 4)
    weights = np.array([1, 2, 3, 4])
    weighted_mean_values = df.apply(lambda x: np.average(x.dropna(), weights=weights[:len(x.dropna())]), axis=0)

    # Calculate frequency of each response (1, 2, 3, 4) for each question
    frequency_data = {}
    for col in df.columns:
        frequency_data[col] = {
            'Frequency 1': (df[col] == 1).sum(),
            'Frequency 2': (df[col] == 2).sum(),
            'Frequency 3': (df[col] == 3).sum(),
            'Frequency 4': (df[col] == 4).sum()
        }

    # Convert frequency data to DataFrame
    frequency_df = pd.DataFrame(frequency_data).T

    # Append Mean, Median, Weighted Mean to the main DataFrame
    df.loc['Mean'] = mean_values
    df.loc['Median'] = median_values
    df.loc['Weighted Mean'] = weighted_mean_values

    # Define the directory and file path
    directory = 'project/results'
    file_path = os.path.join(directory, 'NormalUsers.xlsx')

    # Create the directory if it doesn't exist
    os.makedirs(directory, exist_ok=True)

    # Save to Excel
    with pd.ExcelWriter(file_path, engine='openpyxl') as writer:
        df.to_excel(writer, sheet_name='Survey Analysis')
        frequency_df.to_excel(writer, sheet_name='Frequency Analysis')  # Save frequency data on a new sheet

    flash(f"Data saved to '{file_path}'")
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
