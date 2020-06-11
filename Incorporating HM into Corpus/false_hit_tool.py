import pandas as pd

colsToUse = ["keyword", "false hit [or male]"]
outputCSVHeader = ["keyword", "total count", "hit (not false or ?) count", "hit percentage", "non-male false count", "non-male false percentage", "worth noting count", "worth noting percentage",
                   "? count", "? percentage"]

def parseCols(keyword, falseHitWords, oldInfo):
    totalValue, falseValue, worthNotingValue, unknownValue, maleValue = 1, 0, 0, 0, 0

    if "male" in falseHitWords: maleValue += 1
    elif "false" in falseHitWords: falseValue += 1
    elif "?" in falseHitWords: unknownValue += 1
    if "noting" in falseHitWords: worthNotingValue += 1

    if oldInfo is not None:
        totalValue += oldInfo[1]
        falseValue += oldInfo[2]
        worthNotingValue += oldInfo[3]
        unknownValue += oldInfo[4]

    return [keyword, totalValue, falseValue, worthNotingValue, unknownValue, maleValue]

def getPercentages(values):
    return [values[0], values[1], values[1] - (values[2]+values[4]+values[5]), round(100 * (values[1] - (values[2]+values[4])) / values[1], 1), values[2], round(100 * values[2] / values[1], 1), values[3], round(100 * values[3] / values[1], 1),
            values[4], round(100 * values[4] / values[1], 1)]

def main():
    keywordDict = {}
    dataFrame = pd.read_csv("false_hits.csv", usecols=colsToUse)

    for index, row in dataFrame.iterrows():
        currentKeyword = row["keyword"]

        falseHitWords = []
        if not pd.isna(row["false hit [or male]"]):
            unparsedWords = str(row["false hit [or male]"]).lower()
            falseHitWords = unparsedWords.split(" ")

        keywordDict[currentKeyword] = parseCols(currentKeyword, falseHitWords, keywordDict.get(currentKeyword))

    reportData = []
    for keyword, values in keywordDict.items():
        reportData.append(getPercentages(values))

    newDataFrame = pd.DataFrame(reportData)
    newDataFrame.to_csv("false_hit_percentages.csv", index=False, header=outputCSVHeader)

if __name__ == '__main__':
    main()