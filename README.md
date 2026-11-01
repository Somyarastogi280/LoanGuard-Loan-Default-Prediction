# LoanGuard – Intelligent Loan Default Risk Assessment

An intelligent machine learning-based application designed to predict loan default risk and support better credit risk assessment for financial institutions.

## Project Overview

LoanGuard is a machine learning-powered loan default prediction system that analyses applicant information and estimates the probability of loan repayment difficulties.

The application uses multiple machine learning algorithms to assess credit risk and provides an interactive dashboard where users can enter applicant details, view prediction results, and access application history.

It also incorporates Explainable AI using SHAP and data drift monitoring using Evidently AI to improve model interpretability and monitoring.

## Problem Statement

Financial institutions face significant financial losses due to loan defaults and Non-Performing Assets (NPAs). Traditional loan assessment methods may fail to accurately identify applicants who are likely to experience repayment difficulties.

LoanGuard addresses this challenge by using machine learning models to analyse applicant information, predict default probability, and identify potentially high-risk applicants, helping lenders make more informed lending decisions.

## Project Objectives

* Predict the probability of loan default.
* Identify potentially high-risk loan applicants.
* Compare multiple machine learning algorithms.
* Improve credit risk assessment through data-driven predictions.
* Explain model predictions using SHAP.
* Monitor changes in input data using Evidently AI.
* Maintain application and prediction history.

## Key Features

* **Loan Default Prediction:** Predicts the likelihood of repayment difficulties.
* **Multiple ML Models:** Uses Logistic Regression, Random Forest, and XGBoost.
* **Interactive Dashboard:** Streamlit-based interface for entering applicant details and viewing results.
* **Explainable AI:** SHAP helps interpret the factors influencing predictions.
* **Data Drift Monitoring:** Evidently AI supports monitoring changes in incoming data.
* **Prediction API:** FastAPI provides backend prediction functionality.
* **Application History:** PostgreSQL stores application and prediction records.
* **Docker Support:** Containerized application setup using Docker Compose.

## Technology Stack

| Component            | Technologies                                |
| -------------------- | ------------------------------------------- |
| Programming Language | Python                                      |
| Data Processing      | Pandas, NumPy                               |
| Machine Learning     | Scikit-learn, XGBoost                       |
| ML Algorithms        | Logistic Regression, Random Forest, XGBoost |
| Explainable AI       | SHAP                                        |
| Drift Monitoring     | Evidently AI                                |
| Frontend             | Streamlit                                   |
| Backend              | FastAPI                                     |
| Database             | PostgreSQL                                  |
| Containerization     | Docker, Docker Compose                      |
| Version Control      | Git, GitHub                                 |

## Dataset

**Dataset:** Home Credit Default Risk Dataset

The project uses applicant-related financial and personal information to predict loan repayment difficulties.

**Target Variable: `TARGET`**

* `0` – No repayment difficulties.
* `1` – Applicant experienced repayment difficulties.

The dataset is used for data preprocessing, exploratory data analysis, model training, and prediction.

Dataset source: [Home Credit Default Risk – Kaggle](https://www.kaggle.com/competitions/home-credit-default-risk)

## Machine Learning Models

The project incorporates three machine learning algorithms:

1. **Logistic Regression:** A classification algorithm used as a baseline model.
2. **Random Forest:** An ensemble learning algorithm that combines multiple decision trees.
3. **XGBoost:** A gradient boosting algorithm used for predictive modelling.

The models are used to assess loan default risk.

## System Architecture

The application follows a client-server architecture.

```text
       USER
         |
         v
  STREAMLIT FRONTEND
         |
         v
    FASTAPI BACKEND
         |
         v
   DATA PREPROCESSING
         |
         v
  TRAINED ML MODEL
         |
         v
  DEFAULT PREDICTION
         |
    +----+-----+
    |          |
    v          v
   SHAP     PREDICTION
 EXPLANATION   RESULT
    |          |
    +----+-----+
         |
         v
   STREAMLIT DASHBOARD
         |
         v
     POSTGRESQL
  APPLICATION HISTORY

  EVIDENTLY AI
  DATA DRIFT MONITORING
```

## Project Structure

```text
LoanGuard-Loan-Default-Prediction/
│
├── API/
│   ├── main.py
│   └── main1.py
│
├── DATA/
│   └── application_train.csv
│
├── MODEL/
│   └── final_model.pkl
│
├── NOTEBOOK/
│   └── 01_EDA.ipynb
│
├── REPORTS/
│   └── data_drift_report.html
│
├── STREAMLIT/
│   └── app.py
│
├── Dockerfile
├── compose.yaml
├── REQUIREMENT.txt
└── .gitignore
```

*Note: Some local data and model files may be excluded from the public GitHub repository through `.gitignore`.*

## Installation and Setup

### Prerequisites

* Python 3.11
* Git
* Docker Desktop
* Docker Compose

### 1. Clone the Repository

```bash
git clone https://github.com/Somyarastogi280/LoanGuard-Loan-Default-Prediction.git
```

### 2. Navigate to the Project Directory

```bash
cd LoanGuard-Loan-Default-Prediction
```

### 3. Add Required Local Files

Ensure that the required trained model file is available at:

```text
MODEL/final_model.pkl
```

Also provide the required dataset locally if you want to run the exploratory data analysis notebook.

These files may not be included in the GitHub repository.

### 4. Run Using Docker Compose

Build the Docker images:

```bash
docker compose build
```

Start the application:

```bash
docker compose up -d
```

### 5. Access the Application

| Service                   | Local URL                  |
| ------------------------- | -------------------------- |
| Streamlit Dashboard       | http://localhost:8501      |
| FastAPI Backend           | http://localhost:8000      |
| FastAPI API Documentation | http://localhost:8000/docs |

To stop the containers:

```bash
docker compose down
```

## Explainable AI – SHAP

SHAP (SHapley Additive exPlanations) is integrated to help explain machine learning predictions.

It helps identify which applicant features contribute towards a particular prediction, improving the interpretability of the model.

## Data Drift Monitoring – Evidently AI

Evidently AI is used for data drift monitoring.

It helps identify changes in incoming data distributions compared with reference data, supporting model monitoring and reliability.

## Database Integration

PostgreSQL is integrated to maintain application records and prediction history.

The database supports storing and retrieving application information through the application.

## Expected Business Impact

LoanGuard aims to support financial institutions by:

* Improving identification of potentially high-risk applicants.
* Supporting informed credit risk assessment.
* Providing interpretable machine learning predictions.
* Helping reduce financial exposure caused by loan defaults.

**Project targets:** AUC of at least 85% and a potential 30% reduction in NPAs. These are intended targets, not verified business outcomes.

## Future Scope

* Model performance optimization.
* Integration with additional financial datasets.
* Improved model monitoring and retraining.
* Secure user authentication and role-based access.
* Cloud deployment with persistent database storage.
* Enhanced prediction analytics and reporting.

## References

1. [Home Credit Default Risk Dataset – Kaggle](https://www.kaggle.com/competitions/home-credit-default-risk)
2. [Scikit-learn Documentation](https://scikit-learn.org/stable/)
3. [XGBoost Documentation](https://xgboost.readthedocs.io/)
4. [SHAP Documentation](https://shap.readthedocs.io/)
5. [FastAPI Documentation](https://fastapi.tiangolo.com/)
6. [Streamlit Documentation](https://docs.streamlit.io/)
7. [Evidently AI Documentation](https://docs.evidentlyai.com/)

Author

Somya Rastogi

B.Tech – Electrical and Computer Engineering
ABES Engineering College, Ghaziabad

GitHub: [Somyarastogi280](https://github.com/Somyarastogi280)
LoanGuard – Intelligent Loan Default Risk Assessment
