"""Rate plan definitions and pricing rules for Alectra Utilities."""

# rate structures
TIERED_RATES = {
    'tier1_limit': 1000,  # kWh per month
    'tier1_rate': 0.120,  # $/kWh
    'tier2_rate': 0.142   # $/kWh
}

TOU_RATES = {
    'off_peak': 0.098,   # $/kWh
    'mid_peak': 0.157,   # $/kWh
    'on_peak': 0.203     # $/kWh
}

ULO_RATES = {
    'ultra_low': 0.039,  # $/kWh (11PM-7AM)
    'off_peak': 0.098,   # $/kWh
    'mid_peak': 0.157,   # $/kWh
    'on_peak': 0.391     # $/kWh (4-9PM weekdays)
}


def get_tou_period(hour, day_of_week):
    """
    Classify hour into TOU pricing period.

    Args:
        hour: Hour of day (0-23)
        day_of_week: Day of week (0=Monday, 6=Sunday)

    Returns:
        str: "on_peak", "mid_peak", or "off_peak"
    """
    is_weekend = day_of_week >= 5

    if is_weekend:
        return "off_peak"

    # weekdays
    if 7 <= hour < 11 or 17 <= hour < 19:
        return "on_peak"
    elif 11 <= hour < 17:
        return "mid_peak"
    else:
        return "off_peak"


def get_ulo_period(hour, day_of_week):
    """
    Classify hour into ULO pricing period.

    Args:
        hour: Hour of day (0-23)
        day_of_week: Day of week (0=Monday, 6=Sunday)

    Returns:
        str: "ultra_low", "on_peak", "mid_peak", or "off_peak"
    """
    is_weekend = day_of_week >= 5

    # ultra-low overnight hours (11PM-7AM every day)
    if hour >= 23 or hour < 7:
        return "ultra_low"

    if is_weekend:
        return "off_peak"

    # weekdays
    if 16 <= hour < 21:  # 4PM-9PM
        return "on_peak"
    elif 11 <= hour < 17:
        return "mid_peak"
    else:
        return "off_peak"
