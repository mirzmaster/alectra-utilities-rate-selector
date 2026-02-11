# Project

A project to evaluate electricity usage by a residential household and select the most cost efficient Alectra Utilities rate plan. Hourly electricity usage is evaluated, usage pattern analyzed, compared to the available rate plans, and the best rate plan recommended.

## Structure
./data/<identifier>/ - contains raw hourly data downloaded from the user's Alectra customer portal
./plans/ - image or text data for all the available rate plans
./scripts/ - all processing scripts
./output/data/ - contains aggregate data for the current analysis run that combines all the raw data
./output/report/ - contains the report with recommendation on the optimal rate plan

## Data aggregation and analysis
- hourly data is provided with one file per day, broken down by hour
- each raw data file includes cost information as well which is not relevant to the recommendation
- aggregated data should take the hourly consumption from all the raw files, with rows per hour, and columns per day
- usage patterns should differentiate between weekdays and weekends

## Conventions
- *Always* use a python venv for python script
- the processing script entrypoint should accept identifier as an input, where identifier is an arbitrary identifier for a given dataset
- plan information is available as text data or as screenshots taken from the Alectra Utilities website
- output report should be in HTML
- each command created should be documented in this CLAUDE.md file in the "Commands" section
- maintain a succint README.md file with project information, project structure, and commands
- README should contain an example for each command

## Commands

### analyze electricity usage
```bash
.venv/bin/python analyze.py <identifier>
```
