import pandas as pd


def main():
    files_df_1 = pd.read_csv("run_4_files.csv")
    filenames_list_1 = list(files_df_1["project_file_name"])

    files_df_2 = pd.read_csv("fixed_duplicates.csv")
    filenames_list_2 = list(files_df_2["project_file_name"])

    for name in filenames_list_2:
        if name not in filenames_list_1:
            print(name)

if __name__ == '__main__':
    main()