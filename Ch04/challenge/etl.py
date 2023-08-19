#%%
import pandas as pd
import ipaddress
import http
import sqlite3
from datetime import datetime
from dateutil import parser

# Function to validate IP address
def validate_ip(ip):
    try:
        ipaddress.ip_address(ip)
        return True
    except ValueError:
        return False

# Function to validate time
def validate_time(time):
    now = pd.Timestamp.now()
    return pd.Timestamp.min <= time <= now

# Define the CSV file and database parameters
csv_filename = 'traffic.csv'
db_filename = 'traffic.db'

# Read CSV file into a Pandas DataFrame
df = pd.read_csv(csv_filename)

# Convert 'time' column to Timestamp using dateutil.parser
df['time'] = df['time'].apply(parser.parse)

# Filter out rows with invalid datetime values
df = df.dropna(subset=['time'])

# Validate rows and filter out invalid ones
df['is_valid'] = (
    df.apply(lambda row:
        validate_ip(row['ip']) and
        validate_time(row['time']) and
        row['path'] != '' and
        str(row['status']) in http.HTTPStatus.__members__ and
        str(row['size']) != '' and int(row['size']) >= 0,
        axis=1
    )
)
valid_rows = df[df['is_valid']]
invalid_rows = df[~df['is_valid']]

# Calculate bad row percentage
total_rows = len(valid_rows) + len(invalid_rows)
bad_row_percentage = (len(invalid_rows) / total_rows) * 100

# Check if bad row percentage exceeds threshold
if bad_row_percentage <= 5:
    # Create SQLite database and table
    connection = sqlite3.connect(db_filename)
    valid_rows.drop(columns=['is_valid'], inplace=True)
    valid_rows.to_sql('traffic', connection, if_exists='replace', index=False)
    connection.close()

    print("ETL process completed successfully.")
else:
    print("ETL process failed due to a high percentage of bad rows.")

# %%
valid_rows
# %%
