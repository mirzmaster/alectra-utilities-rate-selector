"""Generate HTML report with analysis results."""

import os
from datetime import datetime
from jinja2 import Template


def generate_insights(analysis, results, optimal_plan, validation=None):
    """
    Generate insights based on usage patterns.

    Args:
        analysis: Usage statistics
        results: Cost results for all plans
        optimal_plan: Name of optimal plan
        validation: Cost validation results (optional)

    Returns:
        str: HTML formatted insights
    """
    insights = []

    # overnight usage insight
    ulo_breakdown = analysis.get('ulo_breakdown', {})
    ultra_low_pct = (ulo_breakdown.get('ultra_low', 0) / analysis['total_kwh']) * 100

    if ultra_low_pct > 25:
        insights.append(f"<li>Your overnight usage (11PM-7AM) represents {ultra_low_pct:.1f}% of total consumption, making ULO plan particularly beneficial.</li>")
    elif ultra_low_pct < 10:
        insights.append(f"<li>Your overnight usage (11PM-7AM) is relatively low at {ultra_low_pct:.1f}% of total consumption.</li>")

    # peak usage insight
    tou_breakdown = analysis.get('tou_breakdown', {})
    on_peak_pct = (tou_breakdown.get('on_peak', 0) / analysis['total_kwh']) * 100

    if on_peak_pct > 30:
        insights.append(f"<li>High on-peak usage ({on_peak_pct:.1f}% during 7-11AM and 5-7PM weekdays) increases costs on time-based plans.</li>")
    else:
        insights.append(f"<li>On-peak usage is well-managed at {on_peak_pct:.1f}% of total consumption.</li>")

    # weekend vs weekday
    weekend_avg = analysis['weekend_kwh'] / max(analysis['num_weekends'], 1)
    weekday_avg = analysis['weekday_kwh'] / max(analysis['num_weekdays'], 1)

    if weekend_avg > weekday_avg * 1.2:
        insights.append(f"<li>Weekend consumption is {((weekend_avg / weekday_avg - 1) * 100):.1f}% higher than weekdays, benefiting from weekend off-peak rates.</li>")
    elif weekday_avg > weekend_avg * 1.2:
        insights.append(f"<li>Weekday consumption is {((weekday_avg / weekend_avg - 1) * 100):.1f}% higher than weekends.</li>")

    # tier threshold insight
    monthly_kwh = analysis['monthly_kwh_projected']
    if monthly_kwh > 1000:
        insights.append(f"<li>Projected monthly usage of {monthly_kwh:.0f} kWh exceeds the 1,000 kWh tier threshold, resulting in {(monthly_kwh - 1000):.0f} kWh at the higher tier rate.</li>")
    else:
        insights.append(f"<li>Projected monthly usage of {monthly_kwh:.0f} kWh stays within the lower tier threshold of 1,000 kWh.</li>")

    # cost comparison
    costs = {
        'Tiered': results['tiered']['total_cost'],
        'TOU': results['tou']['total_cost'],
        'ULO': results['ulo']['total_cost']
    }
    sorted_costs = sorted(costs.items(), key=lambda x: x[1])

    if sorted_costs[1][1] - sorted_costs[0][1] < 5:
        insights.append(f"<li>The cost difference between {sorted_costs[0][0]} and {sorted_costs[1][0]} is minimal (${sorted_costs[1][1] - sorted_costs[0][1]:.2f}/month).</li>")
    else:
        insights.append(f"<li>Switching to {optimal_plan} provides clear cost savings of ${sorted_costs[-1][1] - sorted_costs[0][1]:.2f}/month compared to the most expensive option.</li>")

    # validation insights
    if validation:
        accuracy = validation['accuracy_percentage']
        if accuracy >= 95:
            insights.append(f"<li>Cost estimates are highly accurate ({accuracy:.1f}% match with actual billing data).</li>")
        elif accuracy >= 90:
            insights.append(f"<li>Cost estimates show good accuracy ({accuracy:.1f}% match with actual billing data).</li>")
        else:
            insights.append(f"<li>Cost estimates show some deviation from actual billing data ({accuracy:.1f}% match). This may be due to additional fees or rate changes.</li>")

    return '\n'.join(insights)


def generate_report(analysis, results, identifier, enriched_df, validation=None):
    """
    Generate HTML report.

    Args:
        analysis: Usage statistics
        results: Cost results for all plans
        identifier: Dataset identifier
        enriched_df: DataFrame with time metadata
        validation: Cost validation results (optional)

    Returns:
        str: Path to generated report
    """
    # determine optimal plan
    from rate_calculator import determine_optimal_plan
    optimal_plan = determine_optimal_plan(results)

    # calculate savings
    costs = {
        'Tiered': results['tiered']['total_cost'],
        'TOU': results['tou']['total_cost'],
        'ULO': results['ulo']['total_cost']
    }
    min_cost = min(costs.values())
    max_cost = max(costs.values())
    savings = max_cost - min_cost

    # get date range
    start_date = enriched_df['datetime'].min().strftime('%B %d, %Y')
    end_date = enriched_df['datetime'].max().strftime('%B %d, %Y')

    # generate insights
    insights = generate_insights(analysis, results, optimal_plan, validation)

    # load template
    template_path = './templates/report_template.html'
    with open(template_path, 'r') as f:
        template_content = f.read()

    template = Template(template_content)

    # render report
    html_content = template.render(
        identifier=identifier,
        analysis=analysis,
        results=results,
        optimal_plan=optimal_plan,
        savings=savings,
        start_date=start_date,
        end_date=end_date,
        insights=insights,
        validation=validation,
        report_date=datetime.now().strftime('%B %d, %Y at %I:%M %p')
    )

    # save report
    output_dir = './output/report'
    os.makedirs(output_dir, exist_ok=True)

    output_path = os.path.join(output_dir, f'{identifier}_report.html')
    with open(output_path, 'w') as f:
        f.write(html_content)

    return output_path
