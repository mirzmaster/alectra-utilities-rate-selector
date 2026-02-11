"""Analyze electricity usage patterns."""

import pandas as pd
from rate_plans import get_tou_period, get_ulo_period


def add_time_metadata(df):
    """
    Add time-based metadata columns to dataframe.

    Args:
        df: DataFrame with datetime and kwh columns

    Returns:
        DataFrame with additional columns: hour, day_of_week, is_weekend, tou_period, ulo_period
    """
    df = df.copy()

    # extract time components
    df.loc[:, 'hour'] = df['datetime'].dt.hour
    df.loc[:, 'day_of_week'] = df['datetime'].dt.dayofweek
    df.loc[:, 'is_weekend'] = df['day_of_week'] >= 5

    # classify into pricing periods
    df.loc[:, 'tou_period'] = df.apply(
        lambda row: get_tou_period(row['hour'], row['day_of_week']),
        axis=1
    )
    df.loc[:, 'ulo_period'] = df.apply(
        lambda row: get_ulo_period(row['hour'], row['day_of_week']),
        axis=1
    )

    return df


def analyze_patterns(df):
    """
    Analyze usage patterns and generate statistics.

    Args:
        df: DataFrame with time metadata

    Returns:
        dict: Statistics about usage patterns
    """
    total_kwh = df['kwh'].sum()
    num_days = df['datetime'].dt.date.nunique()

    # weekday vs weekend breakdown
    weekday_kwh = df[~df['is_weekend']]['kwh'].sum()
    weekend_kwh = df[df['is_weekend']]['kwh'].sum()

    num_weekdays = df[~df['is_weekend']]['datetime'].dt.date.nunique()
    num_weekends = df[df['is_weekend']]['datetime'].dt.date.nunique()

    # average consumption by hour
    weekday_hourly = df[~df['is_weekend']].groupby('hour')['kwh'].mean().to_dict()
    weekend_hourly = df[df['is_weekend']].groupby('hour')['kwh'].mean().to_dict()

    # consumption by pricing period
    tou_breakdown = df.groupby('tou_period')['kwh'].sum().to_dict()
    ulo_breakdown = df.groupby('ulo_period')['kwh'].sum().to_dict()

    # monthly projection
    monthly_kwh = (total_kwh / num_days) * 30

    return {
        'total_kwh': total_kwh,
        'num_days': num_days,
        'num_weekdays': num_weekdays,
        'num_weekends': num_weekends,
        'weekday_kwh': weekday_kwh,
        'weekend_kwh': weekend_kwh,
        'avg_daily_kwh': total_kwh / num_days,
        'weekday_hourly': weekday_hourly,
        'weekend_hourly': weekend_hourly,
        'tou_breakdown': tou_breakdown,
        'ulo_breakdown': ulo_breakdown,
        'monthly_kwh_projected': monthly_kwh
    }
