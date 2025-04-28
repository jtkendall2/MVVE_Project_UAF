# profileloader.py
#
# Manages loading  user defined voltage profiles from csv file.
#
# Part of the MVVE Project - see README.md for project overview

import pandas as pd

def load_profile(file_path):
    df = pd.read_csv(file_path)
    return list(zip(df["time_ms"], df["voltage"]))  # [(time, voltage), ...]
