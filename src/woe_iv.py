import numpy as np
import pandas as pd


EPSILON = 0.000001


def calculate_woe_iv(
    df,
    feature,
    target="Bad"
):
    """
    Calculate WOE and IV for an already-binned feature.

    WOE convention used in this project:

        WOE = ln(%Good / %Bad)

    Therefore:
        Positive WOE → relatively lower risk
        Negative WOE → relatively higher risk
    """

    temp = df[[feature, target]].copy()

    total_good = (temp[target] == 0).sum()
    total_bad = (temp[target] == 1).sum()

    grouped = (
        temp.groupby(
            feature,
            dropna=False,
            observed=False
        )[target]
        .agg(
            total="count",
            bad="sum"
        )
    )

    grouped["good"] = (
        grouped["total"] - grouped["bad"]
    )

    # Distribution of good and bad
    grouped["dist_good"] = (
        grouped["good"] / total_good
    )

    grouped["dist_bad"] = (
        grouped["bad"] / total_bad
    )

    # Prevent division by zero / log(0)
    grouped["dist_good"] = (
        grouped["dist_good"]
        .replace(0, EPSILON)
    )

    grouped["dist_bad"] = (
        grouped["dist_bad"]
        .replace(0, EPSILON)
    )

    # WOE
    grouped["WOE"] = np.log(
        grouped["dist_good"] /
        grouped["dist_bad"]
    )

    # IV
    grouped["IV"] = (
        (
            grouped["dist_good"] -
            grouped["dist_bad"]
        )
        * grouped["WOE"]
    )

    return grouped


def calculate_total_iv(
    woe_table
):
    """
    Calculate total Information Value.
    """

    return float(
        woe_table["IV"].sum()
    )


def fit_woe_transformer(
    df,
    feature,
    target="Bad",
    n_bins=10
):
    """
    Fit a WOE transformer using training data.

    Numeric variables:
        Quantile bins are created.

    Low-cardinality variables:
        Values are treated as discrete categories.

    Missing values:
        Kept as a separate 'Missing' category.
    """

    temp = df[
        [feature, target]
    ].copy()

    temp["Bin"] = (
        temp[feature]
        .astype(object)
    )

    # Missing values
    temp.loc[
        temp[feature].isna(),
        "Bin"
    ] = "Missing"

    n_unique = (
        temp[feature]
        .nunique()
    )

    # --------------------------------------------------------
    # Discrete / categorical variable
    # --------------------------------------------------------

    if n_unique <= 5:

        non_missing = (
            temp[feature].notna()
        )

        temp.loc[
            non_missing,
            "Bin"
        ] = (
            temp.loc[
                non_missing,
                feature
            ].astype(str)
        )

        bin_edges = None

    # --------------------------------------------------------
    # Numeric variable
    # --------------------------------------------------------

    else:

        non_missing = (
            temp[feature].notna()
        )

        temp.loc[
            non_missing,
            "Bin"
        ], bin_edges = pd.qcut(
            temp.loc[
                non_missing,
                feature
            ],
            q=n_bins,
            retbins=True,
            duplicates="drop"
        )

        bin_edges[0] = -np.inf
        bin_edges[-1] = np.inf

    # --------------------------------------------------------
    # Calculate WOE / IV
    # --------------------------------------------------------

    woe_table = calculate_woe_iv(
        temp,
        "Bin",
        target
    )

    return {
        "bin_edges": bin_edges,
        "woe_table": woe_table
    }


def transform_with_woe(
    df,
    feature,
    transformer
):
    """
    Apply a previously fitted WOE transformer
    to new data.
    """

    result = df.copy()

    bin_edges = transformer[
        "bin_edges"
    ]

    woe_table = transformer[
        "woe_table"
    ]

    # --------------------------------------------------------
    # Discrete / categorical variable
    # --------------------------------------------------------

    if bin_edges is None:

        values = result[feature]

        result["Bin"] = (
            values.astype(object)
        )

        result.loc[
            values.isna(),
            "Bin"
        ] = "Missing"

        result.loc[
            values.notna(),
            "Bin"
        ] = (
            values.loc[
                values.notna()
            ].astype(str)
        )

        woe_dict = (
            woe_table["WOE"]
            .to_dict()
        )

        result[
            f"{feature}_WOE"
        ] = result["Bin"].map(
            woe_dict
        )

    # --------------------------------------------------------
    # Numeric variable
    # --------------------------------------------------------

    else:

        values = result[feature]

        bin_number = np.digitize(
            values.fillna(
                bin_edges[0]
            ),
            bin_edges[1:-1],
            right=True
        )

        bin_number = np.clip(
            bin_number,
            0,
            len(woe_table) - 1
        )

        result[
            f"{feature}_WOE"
        ] = (
            woe_table["WOE"]
            .iloc[bin_number]
            .values
        )

        # Apply Missing WOE
        if "Missing" in woe_table.index:

            result.loc[
                values.isna(),
                f"{feature}_WOE"
            ] = woe_table.loc[
                "Missing",
                "WOE"
            ]

    # --------------------------------------------------------
    # Safety check
    # --------------------------------------------------------

    if result[
        f"{feature}_WOE"
    ].isna().any():

        raise ValueError(
            f"WOE transformation produced "
            f"NaN values for feature: {feature}"
        )

    return result


def get_woe_iv_summary(
    df,
    features,
    target="Bad",
    n_bins=10
):
    """
    Calculate total IV for multiple features.
    """

    results = []

    for feature in features:

        transformer = fit_woe_transformer(
            df,
            feature,
            target=target,
            n_bins=n_bins
        )

        total_iv = calculate_total_iv(
            transformer["woe_table"]
        )

        results.append({
            "Feature": feature,
            "IV": total_iv
        })

    return (
        pd.DataFrame(results)
        .sort_values(
            "IV",
            ascending=False
        )
        .reset_index(drop=True)
    )