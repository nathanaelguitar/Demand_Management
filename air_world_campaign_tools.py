"""
Air World sponsored search analysis toolkit.

This module provides boilerplate helpers for the Unit 3 Air World case:
- loading the workbook
- cleaning campaign data
- computing row-level and aggregate KPIs
- producing pivot-style summaries by search engine and keyword

The case instructions explicitly say to compute summary metrics from aggregated
tables rather than averaging row-level ratios. The aggregate summary functions in
this module follow that rule.
"""

from __future__ import annotations

from pathlib import Path
from typing import Iterable, Optional

import pandas as pd

DEFAULT_SHEET_NAME = "Air World Data"
DEFAULT_HEADER_ROW = 4  # zero-indexed row in pandas, Excel row 5
NUMERIC_COLUMNS = ["Impressions", "Clicks", "Transactions", "Click Charges", "Revenue"]


def _safe_divide(numerator: pd.Series, denominator: pd.Series) -> pd.Series:
    """Return a zero-filled quotient while avoiding divide-by-zero issues."""
    return numerator.div(denominator.replace(0, pd.NA)).fillna(0)


def load_air_world_data(
    filepath: str,
    sheet_name: str = DEFAULT_SHEET_NAME,
    header_row: int = DEFAULT_HEADER_ROW,
) -> pd.DataFrame:
    """
    Load the Air World dataset from Excel and clean the core fields.

    Args:
        filepath: Path to the Air World workbook.
        sheet_name: Sheet to load.
        header_row: Zero-indexed row containing the true column headers.

    Returns:
        Cleaned campaign DataFrame.
    """
    path = Path(filepath)
    if not path.exists():
        raise FileNotFoundError(f"Excel file not found: {filepath}")

    df = pd.read_excel(path, sheet_name=sheet_name, header=header_row)

    unnamed = [col for col in df.columns if str(col).startswith("Unnamed")]
    if unnamed:
        df = df.drop(columns=unnamed)

    df.columns = [str(col).strip() for col in df.columns]

    for col in NUMERIC_COLUMNS:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors="coerce").fillna(0)

    for col in ["Search Engine", "Keyword"]:
        if col in df.columns:
            df[col] = df[col].astype(str).str.strip()

    return df.dropna(how="all").reset_index(drop=True)


def add_derived_metrics(df: pd.DataFrame) -> pd.DataFrame:
    """
    Add row-level advertising metrics.

    Metrics:
    - CTR = Clicks / Impressions
    - Conversion Rate = Transactions / Clicks
    - CPC = Click Charges / Clicks
    - Revenue per Click = Revenue / Clicks
    - Revenue per Transaction = Revenue / Transactions
    - Profit = Revenue - Click Charges
    - ROI = Profit / Click Charges
    """
    out = df.copy()

    out["CTR"] = _safe_divide(out["Clicks"], out["Impressions"])
    out["Conversion Rate"] = _safe_divide(out["Transactions"], out["Clicks"])
    out["CPC"] = _safe_divide(out["Click Charges"], out["Clicks"])
    out["Revenue per Click"] = _safe_divide(out["Revenue"], out["Clicks"])
    out["Revenue per Transaction"] = _safe_divide(out["Revenue"], out["Transactions"])
    out["Profit"] = out["Revenue"] - out["Click Charges"]
    out["ROI"] = _safe_divide(out["Profit"], out["Click Charges"])

    return out


def filter_data(
    df: pd.DataFrame,
    search_engines: Optional[Iterable[str]] = None,
    keywords: Optional[Iterable[str]] = None,
    min_clicks: Optional[int] = None,
    min_impressions: Optional[int] = None,
) -> pd.DataFrame:
    """Filter campaign data by engine, keyword, and minimum activity thresholds."""
    out = df.copy()

    if search_engines is not None:
        out = out[out["Search Engine"].isin(set(search_engines))]

    if keywords is not None:
        out = out[out["Keyword"].isin(set(keywords))]

    if min_clicks is not None:
        out = out[out["Clicks"] >= min_clicks]

    if min_impressions is not None:
        out = out[out["Impressions"] >= min_impressions]

    return out


def pivot_sum_by_engine(df: pd.DataFrame) -> pd.DataFrame:
    """Return a pivot-style search engine summary using sums."""
    return (
        df.groupby("Search Engine", dropna=False)[NUMERIC_COLUMNS]
        .sum()
        .sort_index()
    )


def pivot_mean_by_engine(df: pd.DataFrame) -> pd.DataFrame:
    """Return a pivot-style search engine summary using averages."""
    return (
        df.groupby("Search Engine", dropna=False)[NUMERIC_COLUMNS]
        .mean()
        .sort_index()
    )


def engine_performance_summary(df: pd.DataFrame) -> pd.DataFrame:
    """Return search engine level KPIs built from aggregated campaign totals."""
    summary = pivot_sum_by_engine(df).copy()

    summary["CTR"] = _safe_divide(summary["Clicks"], summary["Impressions"])
    summary["Conversion Rate"] = _safe_divide(summary["Transactions"], summary["Clicks"])
    summary["TCR"] = summary["Conversion Rate"]
    summary["TPI"] = _safe_divide(summary["Transactions"], summary["Impressions"])
    summary["CPC"] = _safe_divide(summary["Click Charges"], summary["Clicks"])
    summary["CPI"] = _safe_divide(summary["Click Charges"], summary["Impressions"])
    summary["CPT"] = _safe_divide(summary["Click Charges"], summary["Transactions"])
    summary["Revenue per Click"] = _safe_divide(summary["Revenue"], summary["Clicks"])
    summary["Revenue per Transaction"] = _safe_divide(summary["Revenue"], summary["Transactions"])
    summary["Profit"] = summary["Revenue"] - summary["Click Charges"]
    summary["ROI"] = _safe_divide(summary["Profit"], summary["Click Charges"])

    return summary


def keyword_performance_summary(df: pd.DataFrame, min_clicks: int = 0) -> pd.DataFrame:
    """Return keyword-level KPIs ranked by profit and revenue."""
    summary = df.groupby("Keyword", dropna=False)[NUMERIC_COLUMNS].sum()

    summary["CTR"] = _safe_divide(summary["Clicks"], summary["Impressions"])
    summary["Conversion Rate"] = _safe_divide(summary["Transactions"], summary["Clicks"])
    summary["TCR"] = summary["Conversion Rate"]
    summary["TPI"] = _safe_divide(summary["Transactions"], summary["Impressions"])
    summary["CPC"] = _safe_divide(summary["Click Charges"], summary["Clicks"])
    summary["CPI"] = _safe_divide(summary["Click Charges"], summary["Impressions"])
    summary["CPT"] = _safe_divide(summary["Click Charges"], summary["Transactions"])
    summary["Revenue per Click"] = _safe_divide(summary["Revenue"], summary["Clicks"])
    summary["Revenue per Transaction"] = _safe_divide(summary["Revenue"], summary["Transactions"])
    summary["Profit"] = summary["Revenue"] - summary["Click Charges"]
    summary["ROI"] = _safe_divide(summary["Profit"], summary["Click Charges"])

    if min_clicks > 0:
        summary = summary[summary["Clicks"] >= min_clicks]

    return summary.sort_values(["Profit", "Revenue"], ascending=False)


def sort_summary(summary_df: pd.DataFrame, metric: str, ascending: bool = False) -> pd.DataFrame:
    """Sort a summary table by a chosen metric."""
    if metric not in summary_df.columns:
        raise ValueError(f"{metric!r} is not a column in the provided summary.")
    return summary_df.sort_values(metric, ascending=ascending)


def top_keywords(
    df: pd.DataFrame,
    metric: str = "Profit",
    n: int = 10,
    min_clicks: int = 5,
) -> pd.DataFrame:
    """Return the top N keywords by the selected metric."""
    summary = keyword_performance_summary(df, min_clicks=min_clicks)
    if metric not in summary.columns:
        raise ValueError(f"{metric!r} is not a valid keyword summary metric.")
    return summary.sort_values(metric, ascending=False).head(n)


def bottom_keywords(
    df: pd.DataFrame,
    metric: str = "Profit",
    n: int = 10,
    min_clicks: int = 5,
) -> pd.DataFrame:
    """Return the bottom N keywords by the selected metric."""
    summary = keyword_performance_summary(df, min_clicks=min_clicks)
    if metric not in summary.columns:
        raise ValueError(f"{metric!r} is not a valid keyword summary metric.")
    return summary.sort_values(metric, ascending=True).head(n)


def overall_campaign_kpis(df: pd.DataFrame) -> pd.Series:
    """Return campaign-wide KPI totals and rates."""
    impressions = df["Impressions"].sum()
    clicks = df["Clicks"].sum()
    transactions = df["Transactions"].sum()
    cost = df["Click Charges"].sum()
    revenue = df["Revenue"].sum()
    profit = revenue - cost

    return pd.Series(
        {
            "Impressions": impressions,
            "Clicks": clicks,
            "Transactions": transactions,
            "Click Charges": cost,
            "Revenue": revenue,
            "CTR": clicks / impressions if impressions else 0,
            "Conversion Rate": transactions / clicks if clicks else 0,
            "CPC": cost / clicks if clicks else 0,
            "Revenue per Click": revenue / clicks if clicks else 0,
            "Revenue per Transaction": revenue / transactions if transactions else 0,
            "Profit": profit,
            "ROI": profit / cost if cost else 0,
        }
    )


def compare_search_engines(df: pd.DataFrame, metric: str = "Profit") -> pd.DataFrame:
    """Return engine KPIs ranked by the selected metric."""
    summary = engine_performance_summary(df)
    if metric not in summary.columns:
        raise ValueError(f"{metric!r} is not a valid engine metric.")
    return summary.sort_values(metric, ascending=False)


def campaign_spend_share_by_engine(df: pd.DataFrame) -> pd.Series:
    """Return each search engine's share of total click charges."""
    summary = pivot_sum_by_engine(df)
    total_cost = summary["Click Charges"].sum()
    if total_cost == 0:
        return pd.Series(0, index=summary.index, dtype="float64")
    return summary["Click Charges"] / total_cost


def top_keywords_by_clicks(
    df: pd.DataFrame,
    n: int = 10,
    contribution_margin_pct: float = 1.0,
) -> pd.DataFrame:
    """
    Return the top keywords by clicks across all search engines.

    The case study asks for ROA with contribution margin set to 100%, so the
    default `contribution_margin_pct` is 1.0.
    """
    summary = keyword_performance_summary(df, min_clicks=0).copy()
    summary["ROA"] = _safe_divide(
        (summary["Revenue"] * contribution_margin_pct) - summary["Click Charges"],
        summary["Click Charges"],
    )
    ordered = summary.sort_values(["Clicks", "Revenue"], ascending=[False, False])
    return ordered.head(n)


def top_keywords_by_metric(df: pd.DataFrame, metric: str, n: int = 5) -> pd.DataFrame:
    """Return the top keywords across search engines for a chosen aggregate metric."""
    summary = df.groupby("Keyword", dropna=False)[NUMERIC_COLUMNS].sum()
    if metric not in summary.columns:
        raise ValueError(f"{metric!r} must be one of {NUMERIC_COLUMNS!r}.")
    return summary.sort_values(metric, ascending=False).head(n)


def keyword_engine_matrix(
    df: pd.DataFrame,
    values: str = "Revenue",
    aggfunc: str = "sum",
    fill_value: float = 0,
) -> pd.DataFrame:
    """Return a keyword x search engine pivot table."""
    if values not in df.columns:
        raise ValueError(f"{values!r} is not a column in the data.")

    return pd.pivot_table(
        df,
        index="Keyword",
        columns="Search Engine",
        values=values,
        aggfunc=aggfunc,
        fill_value=fill_value,
    )


def main() -> None:
    """Simple command-line demonstration for local use."""
    workbook = Path("air_world.xlsx")
    if not workbook.exists():
        print("Place the Air World workbook in the project root as 'air_world.xlsx' to run this demo.")
        return

    df = load_air_world_data(str(workbook))
    df = add_derived_metrics(df)

    print("Overall campaign KPIs")
    print(overall_campaign_kpis(df))
    print("\nEngine summary")
    print(engine_performance_summary(df))


if __name__ == "__main__":
    main()
