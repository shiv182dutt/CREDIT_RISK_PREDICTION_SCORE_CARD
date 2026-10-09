from fastapi import FastAPI
from src.predict import predict_credit_risk

app = FastAPI(
    title="Credit Risk PD Model API",
    version="1.0.0"
)


@app.get("/")
def home():
    return {
        "message": "Credit Risk PD Model API is running"
    }


@app.post("/predict")
def predict(input_data: dict):

    result = predict_credit_risk(input_data)

    return result