import pandas as pd
import os
from os import path
import sys

# Given a semicolon-delimited list of interviewee ids return a list of ids in int form
def get_interviewee_ids(ids):
    cleaned_ids = []
    split_ids = ids.split(';')

    for this_id in split_ids:
        this_id = this_id.strip().replace("VEE", "")
        cleaned_ids.append(int(this_id))

    return cleaned_ids

def main():
    df_i = pd.read_csv("interviews.csv")

    assumed_race_col = [""] * 2400

    for i, r in df_i.iterrows():
        ids = get_interviewee_ids(r["interviewee_ids"])
        assumed_race = r["researcher_assumed_race"]

        for this_id in ids:
            assumed_race_col[this_id] = assumed_race

    data = {"researcher_assumed_race": assumed_race_col}
    dataFrame = pd.DataFrame(data)
    dataFrame.to_csv("assumed.csv")


if __name__ == '__main__':
    main()