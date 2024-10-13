# import os
import pandas as pd


# function to select only BO and MO events and intrusion events.
def clean_data(df):
    # Filter rows based on columns: 'provincia', 'TipologiaEvento'
    df = df[
        (
            (df["provincia"].str.contains("BO", regex=False, na=False))
            | (df["provincia"].str.contains("MO", regex=False, na=False))
        )
        & (
            (df["TipologiaEvento"].str.contains("INTR", regex=False, na=False))
            | (df["TipologiaEvento"].str.contains("FURTO", regex=False, na=False))
        )
    ]
    return df


# function to build fields for calculting communication time
def build_time_fields(df_clean):
    df_clean["dataEvento"] = df_clean["dataora"].str[:10]
    df_clean["oraEvento"] = df_clean["dataora"].str[11:19]
    df_clean["dataFiltro"] = df_clean["dataoraFiltro"].str[:10]
    df_clean["oraFiltro"] = df_clean["dataoraFiltro"].str[11:19]

    return df_clean


# curdir = os.getcwd("../data")
# print("Current path is:", curdir)
# Replace 'your_file.xlsx' with the path to your Excel file
df = pd.read_excel("../data/agosto_2024.xlsx")

# To display the first few rows
print(df.head())

# run cleaning code: selects province and antintrsuone/antifurto events
df_clean = clean_data(df.copy())
df_clean.head()

df_clean = build_time_fields(df_clean)
df_clean.head()


df_clean
