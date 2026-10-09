import joblib
import numpy as np
import pandas as pd


# ============================================================
# 1. LOAD MODEL AND WOE TRANSFORMERS
# ============================================================

MODEL_PATH = "outputs/models/champion_logistic_model.pkl"
WOE_PATH = "outputs/models/woe_transformers.pkl"

model = joblib.load(MODEL_PATH)
woe_transformers = joblib.load(WOE_PATH)


# ============================================================
# 2. FEATURES
# ============================================================

FINAL_FEATURES = [
    "Credit_History_Years",
    "Credit_Utilization",
    "Debt_to_Income",
    "Employment_Length_Years",
    "Monthly_Income",
    "Number_of_Delinquencies_30",
    "Number_of_Delinquencies_60",
    "Number_of_Delinquencies_90"
]


WOE_FEATURES = [
    "Credit_History_Years_WOE",
    "Credit_Utilization_WOE",
    "Debt_to_Income_WOE",
    "Employment_Length_Years_WOE",
    "Monthly_Income_WOE",
    "Number_of_Delinquencies_30_WOE",
    "Number_of_Delinquencies_60_WOE",
    "Number_of_Delinquencies_90_WOE"
]


# ============================================================
# 3. WOE TRANSFORMATION
# ============================================================

def transform_with_woe(df, feature, transformer):

    result = df.copy()

    bin_edges = transformer["bin_edges"]
    woe_table = transformer["woe_table"]

    # --------------------------------------------------------
    # Categorical / discrete feature
    # --------------------------------------------------------

    if bin_edges is None:

        values = result[feature]

        # Create bin values
        result["Bin"] = values.astype(object)

        # Missing
        result.loc[
            values.isna(),
            "Bin"
        ] = "Missing"

        # Non-missing values
        result.loc[
            values.notna(),
            "Bin"
        ] = values.loc[
            values.notna()
        ].astype(str)

        # WOE dictionary
        woe_dict = woe_table["WOE"].to_dict()

        # First attempt
        result[f"{feature}_WOE"] = result["Bin"].map(woe_dict)

        # ----------------------------------------------------
        # Robust numeric/string matching
        # ----------------------------------------------------

        if result[f"{feature}_WOE"].isna().any():

            for index in result.index:

                if pd.isna(
                    result.loc[
                        index,
                        f"{feature}_WOE"
                    ]
                ):

                    bin_value = result.loc[
                        index,
                        "Bin"
                    ]

                    # Try exact string match
                    if str(bin_value) in woe_dict:

                        result.loc[
                            index,
                            f"{feature}_WOE"
                        ] = woe_dict[
                            str(bin_value)
                        ]

                    # Try numeric match
                    else:

                        try:

                            numeric_value = float(bin_value)

                            for key in woe_dict:

                                try:

                                    if float(key) == numeric_value:

                                        result.loc[
                                            index,
                                            f"{feature}_WOE"
                                        ] = woe_dict[key]

                                        break

                                except (ValueError, TypeError):
                                    continue

                        except (ValueError, TypeError):
                            pass

        # ----------------------------------------------------
        # Missing WOE
        # ----------------------------------------------------

        if "Missing" in woe_table.index:

            result.loc[
                values.isna(),
                f"{feature}_WOE"
            ] = woe_table.loc[
                "Missing",
                "WOE"
            ]

    # --------------------------------------------------------
    # Numeric feature with bins
    # --------------------------------------------------------

    else:

        values = result[feature]

        # Bin non-missing values
        bin_number = np.digitize(
            values.fillna(bin_edges[0]),
            bin_edges[1:-1],
            right=True
        )

        # Get WOE values
        woe_values = woe_table["WOE"].iloc[
            np.clip(
                bin_number,
                0,
                len(woe_table) - 1
            )
        ].values

        result[f"{feature}_WOE"] = woe_values

        # Apply Missing WOE
        if "Missing" in woe_table.index:

            result.loc[
                values.isna(),
                f"{feature}_WOE"
            ] = woe_table.loc[
                "Missing",
                "WOE"
            ]

    return result


# ============================================================
# 4. CREDIT RISK PREDICTION
# ============================================================

def predict_credit_risk(input_data):

    # Convert input dictionary to DataFrame
    df = pd.DataFrame([input_data])

    # --------------------------------------------------------
    # Check required raw features
    # --------------------------------------------------------

    missing_features = [
        feature
        for feature in FINAL_FEATURES
        if feature not in df.columns
    ]

    if missing_features:

        raise ValueError(
            f"Missing required features: {missing_features}"
        )

    # --------------------------------------------------------
    # Convert sentinel values to missing
    # --------------------------------------------------------

    if "Number_of_Delinquencies_30" in df.columns:

        df["Number_of_Delinquencies_30"] = (
            df["Number_of_Delinquencies_30"]
            .replace([96, 98], np.nan)
        )

    # --------------------------------------------------------
    # Apply WOE transformation
    # --------------------------------------------------------

    for feature in FINAL_FEATURES:

        df = transform_with_woe(
            df,
            feature,
            woe_transformers[feature]
        )

    # --------------------------------------------------------
    # Select model features
    # --------------------------------------------------------

    X = df[WOE_FEATURES]

    # --------------------------------------------------------
    # Final NaN check
    # --------------------------------------------------------

    if X.isna().any().any():

        nan_features = X.columns[
            X.isna().any()
        ].tolist()

        raise ValueError(
            f"WOE transformation produced NaN for: "
            f"{nan_features}"
        )

    # --------------------------------------------------------
    # Probability of Default
    # --------------------------------------------------------

    pd_value = model.predict_proba(X)[0, 1]

    # --------------------------------------------------------
    # Standard Scorecard Scaling
    # --------------------------------------------------------

    PDO = 20

    factor = PDO / np.log(2)

    offset = 487.122876

    logit = (
        model.intercept_[0]
        + np.dot(
            X.iloc[0].values,
            model.coef_[0]
        )
    )

    score = offset - factor * logit

    # --------------------------------------------------------
    # Risk Band
    # --------------------------------------------------------

    if score >= 575:

        risk_band = "Low Risk"

    elif score >= 565:

        risk_band = "Medium Risk"

    elif score >= 550:

        risk_band = "High Risk"

    else:

        risk_band = "Very High Risk"

    # --------------------------------------------------------
    # Final Result
    # --------------------------------------------------------

    return {
        "PD": round(float(pd_value), 6),
        "Score": round(float(score), 2),
        "Risk_Band": risk_band
    }


# ============================================================
# 5. LOCAL TEST
# ============================================================

if __name__ == "__main__":

    sample = {

        "Credit_History_Years": 20,

        "Credit_Utilization": 0.72,

        "Debt_to_Income": 0.40,

        "Employment_Length_Years": 5,

        "Monthly_Income": 50000,

        "Number_of_Delinquencies_30": 1,

        "Number_of_Delinquencies_60": 0,

        "Number_of_Delinquencies_90": 0
    }

    result = predict_credit_risk(sample)

    print(result)