import pandas as pd

def main():
    df = pd.read_csv("interviews.csv")

    for i, r in df.iterrows():



if __name__ == '__main__':
    main()