import pandas as pd

def main():
    df = pd.read_csv("false_hits.csv")

    false_hit_count = 0
    for i, r in df.iterrows():
        if not pd.isnull(r["false hit [or male]"]):
            if "false" in r["false hit [or male]"].lower().split(" "):
                false_hit_count += 1

    print("FALSE HITS: {}".format(false_hit_count))


if __name__ == '__main__':
    main()