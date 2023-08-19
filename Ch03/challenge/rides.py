# %%
import pandas as pd

df = pd.read_csv('rides.csv')
df
# %%
# Find out all the rows that have bad values
df[df.isnull().any(axis=1)]
# %%
# - Missing values are not allowed
import numpy as np
mask = df['plate'].str.strip() == ''
df.loc[mask, 'plate'] = np.nan
df.dropna(inplace=True)
# - Distance much be bigger than 0
df = df[df['distance'] > 0]
# %%
df
# %%
# - A plate must be a combination of at least 3 upper case letters or digits
def has_min_upper_or_digits(plate, min_count):
    upper_or_digit_count = sum(1 for char in plate if char.isupper() or char.isdigit())
    return upper_or_digit_count >= min_count
min_count = 3
filtered_df = df[df['plate'].apply(lambda x: has_min_upper_or_digits(x, min_count))]
filtered_df
# %%
