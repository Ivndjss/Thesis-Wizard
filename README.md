# README Documentation for the Survey Analysis Web Application

This document provides an overview of the **Survey Analysis Web Application**, a Flask-based web application designed to collect and analyze survey responses. The application is tailored for evaluating the performance of a handwriting recognition system, but it can be adapted for other survey-based evaluations.

---

## Table of Contents
1. **Introduction**
2. **Features**
3. **Installation**
4. **Usage**
5. **File Structure**
6. **Dependencies**
7. **Limitations and Future Work**

---

## 1. Introduction
The **Survey Analysis Web Application** is a Flask-based web application that allows users to:
- Collect survey responses from multiple respondents.
- Analyze the responses using statistical metrics such as mean, median, weighted mean, and frequency distribution.
- Save the analyzed data to an Excel file for further review.

The application is designed to evaluate the performance of a handwriting recognition system based on a set of predefined questions. However, the structure is flexible and can be adapted for other survey-based evaluations.

---

## 2. Features
- **Dynamic Survey Form:** The application dynamically generates a survey form based on a predefined list of questions.
- **Multiple Respondents:** Supports data collection from multiple respondents in a single session.
- **Data Validation:** Ensures that responses are valid (e.g., integers within the Likert scale range of 1 to 4).
- **Statistical Analysis:** Calculates mean, median, weighted mean, and frequency distribution for each question.
- **Excel Export:** Saves the analyzed data to an Excel file with two sheets:
  - **Survey Analysis:** Contains raw data, mean, median, and weighted mean.
  - **Frequency Analysis:** Contains the frequency distribution of responses for each question.
- **User Feedback:** Provides flash messages for successful data submission or errors.

---

## 3. Installation
To run the application, follow these steps:

1. **Clone the Repository:**
   ```bash
   git clone <repository-url>
   cd <repository-folder>
   ```

2. **Install Dependencies:**
   Ensure you have Python installed, then install the required libraries using pip:
   ```bash
   pip install flask pandas numpy openpyxl
   ```

3. **Run the Application:**
   ```bash
   python app.py
   ```

4. **Access the Application:**
   Open your web browser and navigate to `http://127.0.0.1:5000`.

---

## 4. Usage
1. **Home Page:**
   - The home page (`/`) displays the survey form with a list of questions.
   - Enter the number of respondents and provide responses for each question using the Likert scale (1 to 4).

2. **Submit Responses:**
   - Click the "Submit" button to process the responses.
   - The application validates the responses and calculates statistical metrics.

3. **View Results:**
   - After submission, the analyzed data is saved to an Excel file (`project/results/NormalUsers.xlsx`).
   - A success message is displayed on the home page.

4. **Error Handling:**
   - If invalid data is entered (e.g., non-integer values or values outside the Likert scale), an error message is displayed, and the user is redirected to the home page.

---

## 5. File Structure
The application consists of the following files and folders:
- **`app.py`:** The main Flask application file.
- **`templates/`:** Contains HTML templates for rendering the web pages.
  - **`index.html`:** The home page template displaying the survey form.
- **`project/results/`:** Directory where the Excel file with analyzed data is saved.

---

## 6. Dependencies
The application requires the following Python libraries:
- **Flask:** For building the web application.
- **Pandas:** For data manipulation and analysis.
- **NumPy:** For numerical calculations.
- **OpenPyXL:** For saving data to Excel files.

Install the dependencies using:
```bash
pip install flask pandas numpy openpyxl
```

---

## 7. Limitations and Future Work
- **Current Limitations:**
  - The application is designed for a specific set of questions. Modifying the questions requires changes to the `questions` list in the code.
  - The Excel file path and directory are hardcoded and may need to be adjusted for different environments.
  - The weighted mean calculation assumes equal weights for all responses.

- **Future Enhancements:**
  - Add support for customizable questions and weights.
  - Implement user authentication to restrict access to the survey form.
  - Add visualizations (e.g., charts) for better data interpretation.
  - Support additional file formats (e.g., CSV) for exporting data.

