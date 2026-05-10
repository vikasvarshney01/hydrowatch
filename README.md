# HydroWatch: Water Quality Monitoring and Prediction System
![Hydrowatch](https://github.com/Satwik-uppada/HydroWatch-Water-Quality-Monitoring-and-Prediction-System/assets/92086645/e91cbfee-db83-453f-a24b-ffb76aee463d)

Welcome to the Water Quality Monitoring and Prediction System! This project aims to provide a user-friendly web application for monitoring and predicting water quality using machine learning models. Below is a detailed explanation of each component of the project, including a comprehensive analysis of the Jupyter Notebook used for model training and selection.

`Access here:` [hydrowatch.streamlit.app](https://hydrowatch.streamlit.app/)


---
## Table of Contents
- [Project Overview](#project-overview)
- [Jupyter Notebook: Model Training and Selection](#jupyter-notebook-model-training-and-selection)
  - [Why Random Forest?](#why-random-forest)
- [Web Application Components](#web-application-components)
  - [Home Page](#home-page)
  - [Model Prediction Page](#model-prediction-page)
  - [Database Page](#database-page)
  - [Database Creation](#database-creation)
  - [User Account Page](#user-account-page)



---
## Project Overview
The Water Quality Monitoring and Prediction System is designed to provide real-time monitoring and prediction of water quality based on various parameters. It leverages machine learning models to analyze and predict the safety of water, offering an easy-to-use interface for users.



---
## Jupyter Notebook: Model Training and Selection

### 355 ML.ipynb

In this Jupyter Notebook, various machine learning models are trained and evaluated to determine the best model for predicting water quality. The following models were tested:

- Logistic Regression
- Decision Tree
- Random Forest
- K-Nearest Neighbors (KNN)
- Support Vector Machine (SVM)
- AdaBoost
- XGBoost
- Gaussian Naive Bayes
- Gradient Boosting

Here are the accuracy scores for each model:

| Model               | Accuracy Score |
|---------------------|----------------|
| Logistic Regression | 80.45%         |
| Decision Tree       | 95.48%         |
| Random Forest       | 97.14%         |
| KNN                 | 87.19%         |
| SVM                 | 76.75%         |
| AdaBoost            | 85.29%         |
| XGBoost             | 96.15%         |
| GaussianNB          | 80.38%         |
| GradientBoosting    | 90.68%         |

### Why Random Forest?

The Random Forest model was selected for building the web application due to its outstanding performance with an accuracy score of 97.14%. Random Forest is an ensemble learning method that operates by constructing multiple decision trees during training and outputs the mode of the classes for classification. Its high accuracy and robustness to overfitting make it an excellent choice for this project.


---
## Web Application Components

### 🏠 Home Page
📄 **File:** [components/home_page.py](components/home_page.py)

The Home Page provides a general introduction and overview of the application. It includes information about the purpose of the project and how users can benefit from it.
![image](https://github.com/Satwik-uppada/HydroWatch-Water-Quality-Monitoring-and-Prediction-System/assets/92086645/6e6290c5-779b-43e3-b05c-e0a85fc8fce9)
Screenshot of the Home Page with a welcoming message.

### 📊 Database Page
📄 **File:** [components/database_page.py](components/database_page.py)

The Database Page displays user-specific historical data and analysis. Users can view their past water quality measurements and see trends over time.
![image](https://github.com/Satwik-uppada/HydroWatch-Water-Quality-Monitoring-and-Prediction-System/assets/92086645/7a765bfb-f57d-4eb5-9436-33a90ff378cf)
Screenshot of the Database Page with sample training data.

### Database Creation
📄 **File:** [components/database_creation.py](components/database_creation.py)

This file handles the creation and management of the database. It includes functions to interact with the database, such as fetching and storing data.

### 🔮 Model Prediction Page
📄 **File:** [components/model_page.py](components/model_page.py)

The Model Prediction Page allows users to input various water quality parameters and get predictions on whether the water is safe or not. It uses the Random Forest model to provide accurate predictions.
#### Prediction page for Guest User
![image](https://github.com/Satwik-uppada/HydroWatch-Water-Quality-Monitoring-and-Prediction-System/assets/92086645/56cb95bb-4fc7-4fa1-8d0b-610d3adbc1db)
#### Prediction page for Registered User
![image](https://github.com/Satwik-uppada/HydroWatch-Water-Quality-Monitoring-and-Prediction-System/assets/92086645/1dfdea48-a352-452f-bf2a-35d184137336)
Screenshot of the Model Prediction Page showing the input form and prediction results.

### 👤 User Account Page
📄 **File:** [components/account_page.py](components/account_page.py)

The User Account Page manages user authentication using Firebase. It includes functions for signing up, signing in, and resetting passwords. It also displays user account information and personalized analysis for logged-in users.
![image](https://github.com/Satwik-uppada/HydroWatch-Water-Quality-Monitoring-and-Prediction-System/assets/92086645/1dfdea48-a352-452f-bf2a-35d184137336)
Screenshot of the User Account Page showing login and signup forms.

They get the personalized analysis report for their input data and prediction over the time.
![image](https://github.com/Satwik-uppada/HydroWatch-Water-Quality-Monitoring-and-Prediction-System/assets/92086645/3d8d9580-ac3b-42b1-87b1-dc5a6e8729c9)

---
## 🎓 Getting Started

To get started with the project, follow these steps:

1. Clone the repository.
2. Install the required libraries.
3. Set up Firebase for authentication.
4. Run the `app.py` file to start the Streamlit web application.

## Requirements

- Python 3.7+
- Streamlit
- sqlite3
- Firebase_admin
- Streamlit_lottie
- pgwalker
- pandas
- numpy
- matplotlib.pyplot
- seaborn
- plotly
- sklearn
- json
- joblib
- requests


---

Feel free to reach out if you have any questions or need further assistance. Enjoy using the Water Quality Monitoring and Prediction System! 🌊🚰

