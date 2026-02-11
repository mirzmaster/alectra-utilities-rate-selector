"""Calculate costs for different rate plans."""

from rate_plans import TIERED_RATES, TOU_RATES, ULO_RATES


def calculate_tiered_cost(analysis):
    """
    Calculate cost under tiered rate plan.

    Args:
        analysis: Dictionary with usage statistics

    Returns:
        dict: Cost breakdown and total
    """
    monthly_kwh = analysis['monthly_kwh_projected']
    tier1_limit = TIERED_RATES['tier1_limit']

    if monthly_kwh <= tier1_limit:
        tier1_kwh = monthly_kwh
        tier2_kwh = 0
    else:
        tier1_kwh = tier1_limit
        tier2_kwh = monthly_kwh - tier1_limit

    tier1_cost = tier1_kwh * TIERED_RATES['tier1_rate']
    tier2_cost = tier2_kwh * TIERED_RATES['tier2_rate']
    total_cost = tier1_cost + tier2_cost

    return {
        'plan': 'Tiered',
        'monthly_kwh': monthly_kwh,
        'tier1_kwh': tier1_kwh,
        'tier2_kwh': tier2_kwh,
        'tier1_cost': tier1_cost,
        'tier2_cost': tier2_cost,
        'total_cost': total_cost
    }


def calculate_tou_cost(analysis):
    """
    Calculate cost under TOU rate plan.

    Args:
        analysis: Dictionary with usage statistics

    Returns:
        dict: Cost breakdown and total
    """
    breakdown = analysis['tou_breakdown']
    num_days = analysis['num_days']

    # calculate cost for actual period
    off_peak_kwh = breakdown.get('off_peak', 0)
    mid_peak_kwh = breakdown.get('mid_peak', 0)
    on_peak_kwh = breakdown.get('on_peak', 0)

    off_peak_cost = off_peak_kwh * TOU_RATES['off_peak']
    mid_peak_cost = mid_peak_kwh * TOU_RATES['mid_peak']
    on_peak_cost = on_peak_kwh * TOU_RATES['on_peak']

    total_cost_actual = off_peak_cost + mid_peak_cost + on_peak_cost

    # project to monthly
    monthly_multiplier = 30 / num_days
    total_cost_monthly = total_cost_actual * monthly_multiplier

    return {
        'plan': 'TOU',
        'monthly_kwh': analysis['monthly_kwh_projected'],
        'off_peak_kwh': off_peak_kwh * monthly_multiplier,
        'mid_peak_kwh': mid_peak_kwh * monthly_multiplier,
        'on_peak_kwh': on_peak_kwh * monthly_multiplier,
        'off_peak_cost': off_peak_cost * monthly_multiplier,
        'mid_peak_cost': mid_peak_cost * monthly_multiplier,
        'on_peak_cost': on_peak_cost * monthly_multiplier,
        'total_cost': total_cost_monthly
    }


def calculate_ulo_cost(analysis):
    """
    Calculate cost under ULO rate plan.

    Args:
        analysis: Dictionary with usage statistics

    Returns:
        dict: Cost breakdown and total
    """
    breakdown = analysis['ulo_breakdown']
    num_days = analysis['num_days']

    # calculate cost for actual period
    ultra_low_kwh = breakdown.get('ultra_low', 0)
    off_peak_kwh = breakdown.get('off_peak', 0)
    mid_peak_kwh = breakdown.get('mid_peak', 0)
    on_peak_kwh = breakdown.get('on_peak', 0)

    ultra_low_cost = ultra_low_kwh * ULO_RATES['ultra_low']
    off_peak_cost = off_peak_kwh * ULO_RATES['off_peak']
    mid_peak_cost = mid_peak_kwh * ULO_RATES['mid_peak']
    on_peak_cost = on_peak_kwh * ULO_RATES['on_peak']

    total_cost_actual = ultra_low_cost + off_peak_cost + mid_peak_cost + on_peak_cost

    # project to monthly
    monthly_multiplier = 30 / num_days
    total_cost_monthly = total_cost_actual * monthly_multiplier

    return {
        'plan': 'ULO',
        'monthly_kwh': analysis['monthly_kwh_projected'],
        'ultra_low_kwh': ultra_low_kwh * monthly_multiplier,
        'off_peak_kwh': off_peak_kwh * monthly_multiplier,
        'mid_peak_kwh': mid_peak_kwh * monthly_multiplier,
        'on_peak_kwh': on_peak_kwh * monthly_multiplier,
        'ultra_low_cost': ultra_low_cost * monthly_multiplier,
        'off_peak_cost': off_peak_cost * monthly_multiplier,
        'mid_peak_cost': mid_peak_cost * monthly_multiplier,
        'on_peak_cost': on_peak_cost * monthly_multiplier,
        'total_cost': total_cost_monthly
    }


def calculate_all_plans(df, analysis):
    """
    Calculate costs for all rate plans.

    Args:
        df: DataFrame with usage data
        analysis: Dictionary with usage statistics

    Returns:
        dict: Results for each plan
    """
    tiered = calculate_tiered_cost(analysis)
    tou = calculate_tou_cost(analysis)
    ulo = calculate_ulo_cost(analysis)

    return {
        'tiered': tiered,
        'tou': tou,
        'ulo': ulo
    }


def determine_optimal_plan(results):
    """
    Determine which plan has the lowest cost.

    Args:
        results: Dictionary with results for each plan

    Returns:
        str: Name of optimal plan
    """
    costs = {
        'Tiered': results['tiered']['total_cost'],
        'TOU': results['tou']['total_cost'],
        'ULO': results['ulo']['total_cost']
    }

    optimal = min(costs, key=costs.get)
    return optimal
