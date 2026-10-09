import pandas as pd
import numpy as np


def clean_data(df):
    """
    Clean the credit risk dataset.

    Parameters
    ----------
    df : pandas.DataFrame
        Raw credit risk data.

    Returns
    -------
    pandas.DataFrame
        Cleaned credit risk data.
    """

    df = df.copy()

    # --------------------------------------------------
    # 1. Convert sentinel values to missing values
    # --------------------------------------------------

    df["Number_of_Delinquencies_30"] = (
        df["Number_of_Delinquencies_30"]
        .replace([96, 98], np.nan)
    )

    # --------------------------------------------------
    # 2. Remove impossible ages
    # --------------------------------------------------

    df = df[
        (df["Age"] >= 18) &
        (df["Age"] <= 100)
    ].copy()

    # --------------------------------------------------
    # 3. Create missing-value indicators
    # --------------------------------------------------

    df["Income_Missing"] = (
        df["Monthly_Income"]
        .isna()
        .astype(int)
    )

    df["DTI_Missing"] = (
        df["Debt_to_Income"]
        .isna()
        .astype(int)
    )

    df["Employment_Length_Missing"] = (
        df["Employment_Length_Years"]
        .isna()
        .astype(int)
    )

    # --------------------------------------------------
    # 4. Impute missing numerical variables
    # --------------------------------------------------

    df["Monthly_Income"] = (
        df["Monthly_Income"]
        .fillna(df["Monthly_Income"].median())
    )

    df["Debt_to_Income"] = (
        df["Debt_to_Income"]
        .fillna(df["Debt_to_Income"].median())
    )

    df["Employment_Length_Years"] = (
        df["Employment_Length_Years"]
        .fillna(
            df["Employment_Length_Years"].median()
        )
    )

    # --------------------------------------------------
    # 5. Cap extreme values
    # --------------------------------------------------

    numeric_cap_columns = [
        "Monthly_Income",
        "Total_Debt",
        "Loan_Amount",
        "Debt_to_Income",
        "Credit_Utilization"
    ]

    for col in numeric_cap_columns:

        lower = df[col].quantile(0.01)
        upper = df[col].quantile(0.99)

        df[col] = df[col].clip(
            lower=lower,
            upper=upper
        )

    return df