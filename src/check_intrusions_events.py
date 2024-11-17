import os
import pandas as pd


# function to select only BO and MO events and intrusion events.
def clean_data(df):
    # Filter rows based on columns: 'provincia', 'TipologiaEvento'
    df = df[
        (
            (df["provincia"].str.contains("BO", regex=False, na=False, case=False))
            | (df["provincia"].str.contains("MO", regex=False, na=False, case=False))
        )
        & (
            (
                df["TipologiaEvento"].str.contains(
                    "INTR", regex=False, na=False, case=False
                )
            )
            | (
                df["TipologiaEvento"].str.contains(
                    "FURTO", regex=False, na=False, case=False
                )
            )
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


# function to calculate event duration in seconds
def calc_duration(df_clean):  # Convert datetime fields to datetime objects
    df_clean["start_datetime"] = pd.to_datetime(
        df_clean["dataEvento"] + " " + df_clean["oraEvento"]
    )
    df_clean["end_datetime"] = pd.to_datetime(
        df_clean["dataFiltro"] + " " + df_clean["oraFiltro"]
    )
    # Calculate duration in seconds
    df_clean["duration_seconds"] = (
        df_clean["end_datetime"] - df_clean["start_datetime"]
    ).dt.total_seconds()
    # Find values less than zero and set them to zero
    df_clean.loc[df_clean["duration_seconds"] < 0, "duration_seconds"] = 0
    # Find values higher than a conventional threshold value (360 sec) and set them to180 sec
    df_clean.loc[df_clean["duration_seconds"] > 360, "duration_seconds"] = 180

    return df_clean


print("Opening dataset to process ...")
# curdir = os.getcwd("../data")
# print("Current path is:", curdir)
# Replace 'your_file.xlsx' with the path to your Excel file
df = pd.read_excel("P:/Lavoro/VSCode/New_project/demo-project/data/settembre_2024.xlsx")

# Assuming you have a file path stored in the variable 'file_path'
file_path = "C:/Users/YourName/Documents/settembre_2024.xlsx"

# Get the base name of the file
file_name = os.path.basename(file_path)

print("File name:", file_name)

# To display the first few rows
print(df.head())

print("Running processing ...\n")
# run cleaning code: selects province and antintrsuone/antifurto events
df_clean = clean_data(df.copy())
df_clean.head()
# run chunk of code to build fields to calculate event duration
df_clean = build_time_fields(df_clean.copy())
df_clean.head()
# calculate event duration
df_clean = calc_duration(df_clean.copy())
df_clean.head()

# Calculate the mean of the 'duration_seconds' column
mean_duration = df_clean["duration_seconds"].mean()
print("Mean duration:", mean_duration)

# Calculate the 85th percentile
percentile_85 = df_clean["duration_seconds"].quantile(0.85)
print("85th percentile:", percentile_85)

# Calculate the total number of items
num_items = len(df_clean["duration_seconds"])
print("Number of items:", num_items)

df_clean.to_excel(
    "P:/Lavoro/VSCode/New_project/demo-project/data/settembre_2024_intr.xlsx",
    index=False,
)
