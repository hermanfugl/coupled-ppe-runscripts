import os
import pandas as pd
from pathlib import Path

from tinkertool.utils.csv_to_ini import df_to_ini

# Perform commands from the script directory pov
script_dir = Path(__file__).parent
os.chdir(script_dir)

# Open the CSV file
input_csv_file = Path('input_files/NorESM3_tuningparameterinfo_PPE_cleaned.csv').resolve()
if not input_csv_file.is_file():
    raise FileNotFoundError(f"Input CSV file '{input_csv_file}' not found.")

# Read the CSV file into a DataFrame
df = pd.read_csv(
    input_csv_file,
    skip_blank_lines=True,
    skiprows=[1]
    )

# TEMPORARY: Exclude rows with parameter file input type i.e. Land
df = df[df['input_type'] != 'parameter_file']

# Make sure that default, min, max are floats
# If it is a string, with _r8, remove the _r8 and convert to float
for col in ['default', 'min', 'max']:
    for row in df.index:
        val = df.at[row, col]
        if isinstance(val, str):
            # Remove _r8 if present
            val = val.replace('_r8', '')
            # Replace unicode minus with standard minus
            val = val.replace('\u2212', '-')
            try:
                val = float(val)
            except ValueError:
                raise ValueError(f"Column '{col}' in row {df['parameter name'][row]} is not a valid float value: {df.at[row, col]}")
        else:
            val = float(val)
        df.at[row, col] = val

# Make sure ndigits is an integer
df['ndigits'] = df['ndigits'].astype(int)

df_to_ini(
    df=df,
    ini_file_path=Path('input_files/NorESM3_tuningparameterinfo_PPE.ini').resolve(),
    section_column='parameter name',
    columns_to_include={
        'component': 'component',
        'module': 'module',
        'parameter description': 'description',
        'default': 'default',
        'min': 'min',
        'max': 'max',
        'sampling': 'sampling',
        'ndigits': 'ndigits',
        'input_type': 'input_type',
        'interdependent_with': 'interdependent_with',
        'last_edited': 'last_edited',
        'Justification': 'justification',
        'Documentation': 'documentation',
    }
)