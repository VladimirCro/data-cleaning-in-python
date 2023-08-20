# %%
import pandas as pd

df = pd.read_csv('workshops.csv')
df
# %%
"""
Fix the data frame. At the end, row should have the following columns:
- start: pd.Timestemap
- end: pd.Timestamp
- name: str
- topic: str (python or go)
- earnings: np.float64
"""
df.drop(index=df.index[:2], inplace=True)
df
# %%
df.loc[1:7, 'Year'] = 2021
df
# %%
df.loc[1:4, 'Month'] = 6
df
# %%
df.loc[5:7, 'Month'] = 7
df
# %%
df.dropna(subset=['Name'], inplace=True)
df
# %%
df['start'] = df.apply(lambda row: pd.to_datetime(f"{int(row['Year'])}-{int(row['Month']):02d}-{int(row['Start']):02d}", format='%Y-%m-%d'), axis=1)
# %%
df['end'] = df.apply(lambda row: pd.to_datetime(f"{int(row['Year'])}-{int(row['Month']):02d}-{int(row['End']):02d}", format='%Y-%m-%d'), axis=1)
df
# %%
columns_to_drop = ['Year', 'Month', 'Start', 'End']
df = df.drop(columns=columns_to_drop)
df
# %%
df_reset = df.reset_index(drop=True)
df
# %%
import re
df['topic'] = df['Name'].str.extract('(go|python)', flags=re.IGNORECASE)
df
# %%
import numpy as np
df['start'] = pd.to_datetime(df['start'])
df['end'] = pd.to_datetime(df['end'])
df['Earnings'] = df['Earnings'].str.replace('[\$,]', '', regex=True).astype(np.float64)
df.dtypes
# %%
df = df[['start', 'end', 'Name', 'topic', 'Earnings']]
# %%
df.rename(columns={'Name': 'name', 'Earnings': 'earnings'}, inplace=True)
df
# %%
