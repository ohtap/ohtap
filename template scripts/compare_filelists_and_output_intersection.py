import pandas as pd

new_csv_header = ["filename"]

def main():

    files_df_1 = pd.read_csv("Arkansas.csv")
    filenames_list_1 = list(files_df_1["filename"])

    files_df_2 = pd.read_csv("Rape_cluster.csv")
    filenames_list_2 = list(files_df_2["filename"])

    new_csv_list = []

    for name in filenames_list_1:
        if name in filenames_list_2:
            new_csv_list.append(name)

    new_csv_name = "new.csv"
    new_csv_df = pd.DataFrame(new_csv_list)
    new_csv_df.to_csv(new_csv_name, index=False, header=new_csv_header)


if __name__ == '__main__':
    main()