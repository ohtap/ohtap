import pandas as pd

def main():
    df_i = pd.read_csv("_cluster_harassment_only_new_metadata.csv")
    cols_to_use = df_i.columns
    df_f = pd.DataFrame(columns=cols_to_use)

    previous_file_name = ""
    for i, r in df_i.iterrows():
        if r["project_file_name"] != previous_file_name:
            previous_file_name = r["project_file_name"]
            df_f = df_f.append(r)

    df_f.to_csv("fixed_duplicates.csv", index=False)


if __name__ == '__main__':
    main()