"""Validate estimated costs against actual costs from billing data."""

import pandas as pd


def calculate_actual_cost(df):
    """
    Calculate total actual cost from raw data.

    Args:
        df: DataFrame with actual_cost column

    Returns:
        dict: {
            'total_actual_cost': float,
            'period_days': int,
            'projected_monthly_actual': float
        }
    """
    # calculate total actual cost
    total_actual_cost = df['actual_cost'].sum()

    # calculate number of days in period
    period_days = (df['datetime'].max() - df['datetime'].min()).days + 1

    # project to monthly cost (30 days)
    projected_monthly_actual = (total_actual_cost / period_days) * 30

    return {
        'total_actual_cost': total_actual_cost,
        'period_days': period_days,
        'projected_monthly_actual': projected_monthly_actual
    }


def validate_estimates(actual_data, estimated_results, num_days):
    """
    Compare estimated costs against actual costs.

    Args:
        actual_data: dict with actual cost info
        estimated_results: dict with all plan estimates
        num_days: number of days in analysis period

    Returns:
        dict: {
            'actual_cost_monthly': float,
            'closest_plan': str,
            'closest_plan_cost': float,
            'accuracy_percentage': float,
            'all_plan_deltas': {
                'tiered': float,
                'tou': float,
                'ulo': float
            },
            'all_plan_accuracy': {
                'tiered': float,
                'tou': float,
                'ulo': float
            }
        }
    """
    actual_monthly = actual_data['projected_monthly_actual']

    # calculate deltas and accuracy for each plan
    all_plan_deltas = {}
    all_plan_accuracy = {}

    for plan_name, plan_data in estimated_results.items():
        estimated_monthly = plan_data['total_cost']
        delta = estimated_monthly - actual_monthly
        accuracy = 100 - abs(delta / actual_monthly * 100)

        all_plan_deltas[plan_name] = delta
        all_plan_accuracy[plan_name] = accuracy

    # find closest matching plan
    closest_plan = min(all_plan_accuracy.items(), key=lambda x: abs(100 - x[1]))
    closest_plan_key = closest_plan[0]
    closest_plan_name = estimated_results[closest_plan_key]['plan']

    return {
        'actual_cost_monthly': actual_monthly,
        'closest_plan': closest_plan_name,
        'closest_plan_key': closest_plan_key,
        'closest_plan_cost': estimated_results[closest_plan_key]['total_cost'],
        'accuracy_percentage': closest_plan[1],
        'all_plan_deltas': all_plan_deltas,
        'all_plan_accuracy': all_plan_accuracy
    }
