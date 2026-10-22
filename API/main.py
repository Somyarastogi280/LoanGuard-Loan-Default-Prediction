from fastapi import FastAPI, HTTPException
from typing import Dict, Any
import pandas as pd
import numpy as np
import joblib
from pathlib import Path
import os
import psycopg2
# ---------------------------------
# FastAPI App
# ---------------------------------
app = FastAPI(
    title="Loan Default Prediction API",
    description="ML-powered loan default prediction using XGBoost",
    version="1.0"
)
# ---------------------------------
# Load Model
# ---------------------------------
BASE_DIR = Path(__file__).resolve().parent
MODEL_PATH = BASE_DIR.parent / "MODEL" / "final_model.pkl"
model = joblib.load(MODEL_PATH)
# Get feature names used during model training
FEATURE_NAMES = list(model.feature_names_in_)
# ---------------------------------
# PostgreSQL Connection
# ---------------------------------
DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "postgresql://loan_user:loan_password@localhost:5432/loan_default_db"
)
def get_db_connection():
    """Create a connection to PostgreSQL."""
    return psycopg2.connect(DATABASE_URL)
# ---------------------------------
# Home Endpoint
# ---------------------------------
@app.get("/")
def home():
    return {
        "message": "Loan Default Prediction API is running"
    }
# ---------------------------------
# Health Check
# ---------------------------------
@app.get("/health")
def health():
    return {
        "status": "healthy"
    }
# ---------------------------------
# Prediction Endpoint
# ---------------------------------
@app.post("/predict")
def predict(loan_data: Dict[str, Any]):
    try:
        # ---------------------------------
        # Create model input
        # ---------------------------------
        input_data = pd.DataFrame(
            np.nan,
            index=[0],
            columns=FEATURE_NAMES
        )
        # Fill the features provided by the user
        for feature, value in loan_data.items():
            if feature in input_data.columns:
                input_data.loc[0, feature] = value
        # ---------------------------------
        # Generate probability
        # ---------------------------------
        probability = float(
            model.predict_proba(input_data)[0][1]
        )
        # ---------------------------------
        # Generate prediction
        # ---------------------------------
        prediction = int(
            model.predict(input_data)[0]
        )
        # ---------------------------------
        # Risk classification
        # ---------------------------------
        if probability >= 0.50:
            risk_level = "High Risk"
        elif probability >= 0.30:
            risk_level = "Medium Risk"
        else:
            risk_level = "Low Risk"
        # ---------------------------------
        # Prepare database values
        # ---------------------------------
        # Convert DAYS_BIRTH to age
        age = None
        if loan_data.get("DAYS_BIRTH") is not None:
            age = round(
                abs(float(loan_data["DAYS_BIRTH"])) / 365
            )
        # Convert DAYS_EMPLOYED to employment years
        employment_years = None
        if loan_data.get("DAYS_EMPLOYED") is not None:
            days_employed = float(
                loan_data["DAYS_EMPLOYED"]
            )
            # Home Credit dataset normally stores employment
            # duration as negative days.
            employment_years = round(
                abs(days_employed) / 365,
                2
            )
        # Convert Y/N values to Boolean
        owns_car = None
        if loan_data.get("FLAG_OWN_CAR") is not None:
            owns_car = (
                str(loan_data["FLAG_OWN_CAR"]).upper() == "Y"
            )
        owns_property = None
        if loan_data.get("FLAG_OWN_REALTY") is not None:
            owns_property = (
                str(loan_data["FLAG_OWN_REALTY"]).upper() == "Y"
            )
        # ---------------------------------
        # Save application to PostgreSQL
        # ---------------------------------
        connection = None
        try:
            connection = get_db_connection()
            cursor = connection.cursor()
            insert_query = """
                INSERT INTO applications (
                    age,
                    children,
                    family_members,
                    annual_income,
                    requested_credit,
                    annuity,
                    goods_price,
                    income_type,
                    employment_years,
                    occupation,
                    housing_type,
                    owns_car,
                    owns_property,
                    ext_source_2,
                    ext_source_3,
                    region_rating,
                    default_prediction,
                    default_probability,
                    risk_level
                )
                VALUES (
                    %s, %s, %s, %s, %s,
                    %s, %s, %s, %s, %s,
                    %s, %s, %s, %s, %s,
                    %s, %s, %s, %s
                )
            """
            values = (
                age,
                loan_data.get("CNT_CHILDREN"),
                loan_data.get("CNT_FAM_MEMBERS"),
                loan_data.get("AMT_INCOME_TOTAL"),
                loan_data.get("AMT_CREDIT"),
                loan_data.get("AMT_ANNUITY"),
                loan_data.get("AMT_GOODS_PRICE"),
                loan_data.get("NAME_INCOME_TYPE"),
                employment_years,
                loan_data.get("OCCUPATION_TYPE"),
                loan_data.get("NAME_HOUSING_TYPE"),
                owns_car,
                owns_property,
                loan_data.get("EXT_SOURCE_2"),
                loan_data.get("EXT_SOURCE_3"),
                loan_data.get("REGION_RATING_CLIENT"),
                prediction,
                round(probability, 3),
                risk_level
            )
            cursor.execute(
                insert_query,
                values
            )
            connection.commit()
            cursor.close()
        except Exception as db_error:
            if connection:
                connection.rollback()
            raise HTTPException(
                status_code=500,
                detail=f"Database error: {str(db_error)}"
            )
        finally:
            if connection:
                connection.close()
        # ---------------------------------
        # Return prediction
        # ---------------------------------
        return {
            "default_prediction": prediction,
            "default_probability": round(probability, 3),
            "risk_level": risk_level
        }
    except HTTPException:
        raise
    except Exception as prediction_error:
        raise HTTPException(
            status_code=500,
            detail=f"Prediction error: {str(prediction_error)}"
        )