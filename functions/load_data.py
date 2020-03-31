import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split

def load_data():
    filename = "C:/Users/ajenk/GitHub/Crime_Data/offenses-standardized.csv"
    fields = ["agency_name", "occurred_date",
          "occurred_time", "firearm_ind", "offense_group", "domestic_violence_ind", "victim_age",
          "victim_race", "victim_ethnicity", "victim_race_condensed", "victim_sex", "clearance_group"]

    crime = pd.read_csv(filename, usecols = fields)
    train, test = train_test_split(crime, test_size=.2, random_state=42)
    train, val = train_test_split(train, test_size=.2, random_state=42)

    return train

def create_binary_target(df):

    df = df.copy()
    df = df[df["clearance_group"] != "Null, Missing, Unclear"]
    df["cleared"] = ~(df["clearance_group"] == "Open & No Arrest-Unspecified")
    df = df.drop(["clearance_group"], axis=1)

    return df

def extract_time_and_date(df):

    df["occurred_date"] = pd.to_datetime(
        df["occurred_date"], infer_datetime_format=True)
    df["occurred_time"] = pd.to_datetime(
        df["occurred_time"], infer_datetime_format=True)

    df["hour"] = df["occurred_time"].dt.hour
    df["hour_zero"] = df["occurred_time"] == pd.to_datetime("00:00")
    df["year"] = df["occurred_date"].dt.year
    df["month"] = df["occurred_date"].dt.month

    df = df.drop(["occurred_date", "occurred_time"], axis=1)

    return df

def clean_age_category(df):

    df["victim_age"] = df["victim_age"].replace({"UNDER 18": "17"})
    df["victim_age"] = df["victim_age"].astype("float")
    df.loc[df["victim_age"] > 100, "victim_age"] = np.NaN

    return df


def separate_black_hispanic(df):

    mask = (df["victim_race"].str.contains(
        "BLACK")) | (df["victim_race"] == "B")

    df.loc[mask, "victim_race_condensed"] = "BLACK"
    df["victim_race_condensed"] = df["victim_race_condensed"].replace(
        {"BLACK/HISPANIC": "HISPANIC"})

    return df

def wrangle():

    df = load_data()
    df = create_binary_target(df)
    df = extract_time_and_date(df)
    df = separate_black_hispanic(df)
    df = clean_age_category(df)

    return df

def generate_most_common(df, feature="agency_name", n=8):
    df_plot = df.copy()
    top_obs = df_plot[feature].value_counts()[:n].index
    df_plot.loc[~df_plot[feature].isin(top_obs), feature] = "Other"

    return df_plot
