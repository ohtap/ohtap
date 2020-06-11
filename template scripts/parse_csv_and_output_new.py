import pandas as pd

new_csv_header = ["Column 1", "Column 2"]

def main():
    df = pd.read_csv("interviews.csv")

    new_csv_list = []

    for i, r in df.iterrows():


    new_csv_name = "new.csv"
    new_csv_df = pd.DataFrame(new_csv_list)
    new_csv_df.to_csv(new_csv_name, index=False, header=new_csv_header)


if __name__ == '__main__':
    main()