#%%
# --- Imports and setup ---
import os
import pandas as pd
from pathlib import Path

# Perform commands from the script directory pov
script_dir = Path(__file__).parent
os.chdir(script_dir)

#%%
# --- define input and output files ---
input_csv_file = script_dir.joinpath('input_files', 'NorESM3_tuningparameterinfo_PPE_cleaned.csv').resolve()
if not input_csv_file.is_file():
    raise FileNotFoundError(f"Input CSV file '{input_csv_file}' not found.")

output_ini_file = script_dir.joinpath('input_files', 'NorESM3_tuningparameterinfo_PPE.ini').resolve()

if output_ini_file.exists():
    print(f"Warning: Output INI file '{output_ini_file}' already exists and will be overwritten.")
output_ini_file.parent.mkdir(parents=True, exist_ok=True)

#%%
# Read the CSV file into a DataFrame
df = pd.read_csv(
    input_csv_file,
    skip_blank_lines=True,
    skiprows=[1]
)
print(f"Read {len(df)} rows from '{input_csv_file}'.")
print(df.head())

# %%
# --- write DataFrame to INI file ---

# The columns to include in the INI file. Mapping from df column names to INI keys.
columns_to_include={
    'component': 'component',
    'module': 'module',
    'parameter description': 'description',
    'default': 'default',
    'scale_fact': 'scale_fact',
    'min': 'min',
    'max': 'max',
    'sampling': 'sampling',
    'ndigits': 'ndigits',
    'last_edited': 'last_edited',
    'Justification': 'justification',
    'Documentation': 'documentation',
    'input_type': 'input_type',
    'interdependent_with': 'interdependent_with',
    'component': 'esm_component'
}
if any(col not in df.columns for col in columns_to_include.keys()):
    missing_cols = [col for col in columns_to_include.keys() if col not in df.columns]
    raise ValueError(f"The following columns specified in columns_to_include are missing from the DataFrame: {missing_cols}")
# Name of the column to use as section headers
header_col_name = 'parameter name'
if header_col_name not in df.columns:
    raise ValueError(f"Section column '{header_col_name}' not found in DataFrame.")
if any(row is None or str(row).strip() == '' for row in df[header_col_name]):
    raise ValueError(f"Section column '{header_col_name}' contains empty values in row {df[header_col_name].index[df[header_col_name].isnull()].tolist()}.")

# Prepare DataFrame with selected columns
ini_df = df[[header_col_name] + list(columns_to_include.keys())]

# Write the DataFrame to an INI file
with output_ini_file.open('w') as ini_file:
    for _, row in ini_df.iterrows():
        section_name = str(row[header_col_name]).strip()
        ini_file.write(f"[{section_name}]\n")
        for col in columns_to_include.keys():
            if isinstance(columns_to_include, dict):
                out_col = columns_to_include[col]
            else:
                out_col = col

            value = row[col]
            if pd.isna(value):
                value = None
            if isinstance(value, (list, tuple)):
                value = ', '.join(map(str, value))
            ini_file.write(f"{out_col} = {value}\n")
        ini_file.write("\n")

print(f"Wrote INI file to '{output_ini_file}'.")