"""Aggregate hourly data into analysis-ready format."""

import os
import pandas as pd


def aggregate_hourly_data(df):
    """
    Pivot data into hourly rows and daily columns.

    Args:
        df: DataFrame with datetime and kwh columns

    Returns:
        DataFrame with 24 rows (hours) and columns per day
    """
    # extract date and hour
    df = df.copy()
    df.loc[:, 'date'] = df['datetime'].dt.date
    df.loc[:, 'hour'] = df['datetime'].dt.hour

    # pivot: hours as rows, dates as columns
    pivoted = df.pivot(index='hour', columns='date', values='kwh')

    return pivoted


def save_aggregated_data(df, identifier):
    """
    Save aggregated data to CSV.

    Args:
        df: Aggregated DataFrame
        identifier: Dataset identifier

    Returns:
        str: Path to saved file
    """
    output_dir = "./output/data"
    os.makedirs(output_dir, exist_ok=True)

    output_path = os.path.join(output_dir, f"{identifier}_aggregated.csv")
    df.to_csv(output_path)

    return output_path
