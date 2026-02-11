"""Load and parse Excel files containing hourly electricity usage."""

import os
import re
from datetime import datetime, timedelta
import pandas as pd
import openpyxl


def extract_date_from_file(filepath):
    """
    Extract date from Excel file content.

    Args:
        filepath: Path to Excel file

    Returns:
        datetime: Date from file metadata
    """
    wb = openpyxl.load_workbook(filepath, data_only=True)
    ws = wb.active

    # date is in row 3, column A (e.g., "Period: Feb 9,2026 ")
    date_cell = ws.cell(row=3, column=1).value

    if isinstance(date_cell, str):
        # extract date from "Period: Feb 9,2026 " format
        try:
            date_str = date_cell.replace('Period:', '').strip()
            date_obj = datetime.strptime(date_str, "%b %d,%Y")
            wb.close()
            return date_obj.date()
        except:
            pass

    wb.close()
    return None


def load_single_file(filepath):
    """
    Load a single Excel file with hourly usage data.

    Args:
        filepath: Path to Excel file

    Returns:
        DataFrame with columns: datetime, kwh
    """
    # extract date from file content
    file_date = extract_date_from_file(filepath)

    if not file_date:
        raise ValueError(f"Could not extract date from {filepath}")

    # read Excel file, skipping metadata rows
    df = pd.read_excel(filepath, skiprows=4)

    # extract time and kWh columns
    df = df.rename(columns={
        'Time': 'time',
        'Units Consumed (kWh)': 'kwh'
    })

    # keep only time and kwh columns
    df = df[['time', 'kwh']].copy()

    # parse time and create full datetime
    df.loc[:, 'hour'] = df['time'].apply(lambda x: int(x.split(':')[0]) if isinstance(x, str) else 0)
    df.loc[:, 'datetime'] = df['hour'].apply(lambda h: datetime.combine(file_date, datetime.min.time()) + timedelta(hours=h))

    # return final dataframe
    result = df[['datetime', 'kwh']].copy()

    return result


def load_all_files(identifier):
    """
    Load all Excel files for a given identifier.

    Args:
        identifier: Dataset identifier (e.g., "test")

    Returns:
        DataFrame with all hourly data combined
    """
    data_dir = f"./data/{identifier}"

    if not os.path.exists(data_dir):
        raise ValueError(f"Data directory not found: {data_dir}")

    # get all Excel files with their dates
    files_with_dates = []
    for filename in os.listdir(data_dir):
        if filename.endswith('.xlsx'):
            filepath = os.path.join(data_dir, filename)
            try:
                file_date = extract_date_from_file(filepath)
                if file_date:
                    files_with_dates.append((file_date, filepath, filename))
            except Exception as e:
                print(f"Error reading date from {filename}: {e}")

    if not files_with_dates:
        raise ValueError(f"No valid Excel files found in {data_dir}")

    # sort by date
    files_with_dates.sort(key=lambda x: x[0])

    # load and combine all files
    all_data = []
    for file_date, filepath, filename in files_with_dates:
        try:
            df = load_single_file(filepath)
            all_data.append(df)
            print(f"Loaded {filename}: {file_date}, {len(df)} hours")
        except Exception as e:
            print(f"Error loading {filename}: {e}")

    if not all_data:
        raise ValueError("No data was successfully loaded")

    # combine all dataframes
    combined = pd.concat(all_data, ignore_index=True)

    # sort by datetime and remove any duplicates
    combined = combined.sort_values('datetime').drop_duplicates(subset='datetime').reset_index(drop=True)

    return combined
