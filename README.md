# Alectra Utilities Rate Optimizer

analyzes hourly electricity usage data to recommend the most cost-efficient rate plan from Alectra Utilities.

## Overview

this tool evaluates residential electricity consumption patterns and compares costs across three available rate plans:

- **tiered**: flat rates with two tiers based on monthly consumption (up to 1,000 kWh and over)
- **time-of-use (TOU)**: variable rates based on time of day and day of week
- **ultra-low overnight (ULO)**: ultra-low rates overnight (11PM-7AM) with higher peak rates

## Project Structure

```
./data/<identifier>/        raw hourly usage data (Excel files)
./output/data/             aggregated data (CSV)
./output/report/           HTML analysis reports
./plans/                   rate plan reference images
./templates/               HTML report template
.venv/                     python virtual environment
requirements.txt           python dependencies
analyze.py                 main entry point
data_loader.py            Excel file parser
data_aggregator.py        data aggregation module
usage_analyzer.py         usage pattern analysis
rate_calculator.py        cost calculation for all plans
cost_validator.py         cost validation against actuals
rate_plans.py             rate definitions and pricing rules
report_generator.py       HTML report generator
```

## Setup

create and activate virtual environment:

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

## Data Preparation

before running the analysis, you need to prepare your electricity usage data:

### 1. download hourly usage data

1. visit the [Alectra Utilities Portal](https://myalectra.alectrautilities.com/portal/#/Usages)
2. navigate to the Usage Overview page
3. download your **hourly usage data** (not daily or monthly)
4. download multiple days of data for more accurate analysis (recommended: 21+ days)

### 2. organize data files

create a subfolder under `data/` with an identifier of your choice:

```bash
mkdir -p data/<identifier>
```

place all downloaded Excel files in this directory:

```bash
data/
└── <identifier>/
    ├── Usage_9541175022.xlsx
    ├── Usage_9541175022(1).xlsx
    ├── Usage_9541175022(2).xlsx
    └── ...
```

### 3. verify rate structures

ensure the rates in `rate_plans.py` are current:

1. check [Alectra Utilities rates page](https://www.alectrautilities.com/residential-rates) for the latest pricing
2. update `rate_plans.py` if rates have changed
3. rate structures may change seasonally or annually

**note:** outdated rates will result in inaccurate cost projections.

## Usage

analyze electricity usage data and generate a report:

```bash
.venv/bin/python analyze.py <identifier>
```

### Example

```bash
.venv/bin/python analyze.py test
```

this will:
1. load all Excel files from `./data/test/`
2. aggregate hourly consumption data
3. analyze usage patterns (weekday vs weekend, peak vs off-peak)
4. calculate projected monthly costs for all three rate plans
5. validate estimates against actual billing data
6. generate an HTML report with recommendations

**outputs:**
- `./output/data/test_aggregated.csv` - hourly consumption matrix (24 hours × days)
- `./output/report/test_report.html` - comprehensive analysis report with cost comparison

## Input Data Format

each Excel file should contain:
- row 3: date in format "Period: MMM DD,YYYY"
- row 5: headers (Time, Cost($), Units Consumed (kWh))
- rows 6-29: 24 hourly records

## Rate Plans

### tiered
- tier 1: $0.120/kWh (up to 1,000 kWh/month)
- tier 2: $0.142/kWh (over 1,000 kWh/month)

### time-of-use (TOU)
- off-peak: $0.098/kWh (weekends all day, weeknights)
- mid-peak: $0.157/kWh (weekdays 11AM-5PM)
- on-peak: $0.203/kWh (weekdays 7-11AM, 5-7PM)

### ultra-low overnight (ULO)
- ultra-low: $0.039/kWh (11PM-7AM every day)
- off-peak: $0.098/kWh (weekends daytime)
- mid-peak: $0.157/kWh (weekdays 11AM-4PM)
- on-peak: $0.391/kWh (weekdays 4-9PM)

## Report Contents

the generated HTML report includes:
- recommended optimal rate plan
- projected monthly costs for all plans
- total and average consumption statistics
- weekday vs weekend usage breakdown
- detailed cost breakdown by pricing period
- cost validation comparing estimates against actual billing data
- identification of current rate plan based on actual costs
- usage pattern insights and recommendations

## Requirements

- python 3.8+
- openpyxl==3.1.5
- pandas==2.2.3
- jinja2==3.1.4
