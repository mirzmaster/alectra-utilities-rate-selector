#!/usr/bin/env python3
"""
Electricity rate analysis tool.

Analyzes hourly electricity usage data and recommends the optimal rate plan.
"""

import sys
import argparse
from data_loader import load_all_files
from data_aggregator import aggregate_hourly_data, save_aggregated_data
from usage_analyzer import add_time_metadata, analyze_patterns
from rate_calculator import calculate_all_plans, determine_optimal_plan
from report_generator import generate_report


def main():
    """Main entry point for rate analysis."""
    parser = argparse.ArgumentParser(
        description='Analyze electricity usage and recommend optimal rate plan'
    )
    parser.add_argument(
        'identifier',
        help='Dataset identifier (e.g., "test")'
    )

    args = parser.parse_args()
    identifier = args.identifier

    print(f"\n=== Electricity Rate Analysis ===")
    print(f"Dataset: {identifier}\n")

    # step 1: load data
    print("Step 1: Loading data...")
    try:
        df = load_all_files(identifier)
        print(f"✓ Loaded {len(df)} hourly records\n")
    except Exception as e:
        print(f"✗ Error loading data: {e}")
        sys.exit(1)

    # step 2: aggregate data
    print("Step 2: Aggregating data...")
    try:
        aggregated = aggregate_hourly_data(df)
        csv_path = save_aggregated_data(aggregated, identifier)
        print(f"✓ Saved aggregated data: {csv_path}\n")
    except Exception as e:
        print(f"✗ Error aggregating data: {e}")
        sys.exit(1)

    # step 3: analyze patterns
    print("Step 3: Analyzing usage patterns...")
    try:
        enriched_df = add_time_metadata(df)
        analysis = analyze_patterns(enriched_df)
        print(f"✓ Total consumption: {analysis['total_kwh']:.1f} kWh over {analysis['num_days']} days")
        print(f"✓ Projected monthly: {analysis['monthly_kwh_projected']:.1f} kWh\n")
    except Exception as e:
        print(f"✗ Error analyzing patterns: {e}")
        sys.exit(1)

    # step 4: calculate costs
    print("Step 4: Calculating costs for all rate plans...")
    try:
        results = calculate_all_plans(enriched_df, analysis)
        optimal = determine_optimal_plan(results)

        print(f"✓ Tiered: ${results['tiered']['total_cost']:.2f}/month")
        print(f"✓ TOU: ${results['tou']['total_cost']:.2f}/month")
        print(f"✓ ULO: ${results['ulo']['total_cost']:.2f}/month")
        print(f"\n→ Optimal plan: {optimal}\n")
    except Exception as e:
        print(f"✗ Error calculating costs: {e}")
        sys.exit(1)

    # step 5: generate report
    print("Step 5: Generating report...")
    try:
        report_path = generate_report(analysis, results, identifier, enriched_df)
        print(f"✓ Report generated: {report_path}\n")
    except Exception as e:
        print(f"✗ Error generating report: {e}")
        sys.exit(1)

    print("=== Analysis Complete ===\n")
    print(f"View your report: {report_path}")


if __name__ == '__main__':
    main()
