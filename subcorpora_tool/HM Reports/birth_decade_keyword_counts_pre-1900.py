import pandas as pd

new_csv_header = ["keyword", "All N", "All %", "AA N", "AA %", "HM N", "HM %"]

term_dictionary = {"all": "All",
                   "anita hill" : "Hill and Thomas",
                   "clarence thomas": "Hill and Thomas",
                   "child abuse": "Child Abuse/Incest",
                   "incest": "Child Abuse/Incest",
                   "incested": "Child Abuse/Incest",
                   "incestuous": "Child Abuse/Incest",
                   "anti-rape": "Anti-rape",
                   "harassment": "Harassment",
                   "harass": "Harassment",
                   "harassed": "Harassment",
                   "harasser": "Harassment",
                   "harasses": "Harassment",
                   "harassing": "Harassment",
                   "harassments": "Harassment",
                   "pedophile": "Pedophil*",
                   "pedophilia": "Pedophil*",
                   "playboy": "Playboy",
                   "rape": "Sexual Violence/Rap*",
                   "raped": "Sexual Violence/Rap*",
                   "rapes": "Sexual Violence/Rap*",
                   "rapist": "Sexual Violence/Rap*",
                   "raping": "Sexual Violence/Rap*",
                   "sex abuse": "Sexual Abuse",
                   "sexual abuse": "Sexual Abuse",
                   "sexually abuse": "Sexual Abuse",
                   "sexual assault": "Sexual Violence/Rap*",
                   "sexual violence": "Sexual Violence/Rap*",
                   "sexist violence": "Sexual Violence/Rap*",
                   "title ix": "Title IX",
                   "attack": "Attack",
                   "bestiality": "Bestiality",
                   "brutalized": "Brutalized",
                   "fondled": "Fondl*",
                   "fondling": "Fondl*",
                   "hanky panky": "Hanky Panky",
                   "fellating": "Fellat*",
                   "insult": "Insult",
                   "interfered with her": "Interfered with her",
                   "ladies man": "Ladies' Man",
                   "ladies' man": "Ladies' Man",
                   "lady's man": "Ladies' Man",
                   "molest": "Molest*",
                   "molestation": "Molest*",
                   "molestations": "Molest*",
                   "molested": "Molest*",
                   "molester": "Molest*",
                   "molesters": "Molest*",
                   "molesting": "Molest*",
                   "molests": "Molest*",
                   "outrage": "Outrage",
                   "pinched": "Pinched",
                   "seduce": "Seduc*",
                   "seduction": "Seduc*",
                   "sex offender": "Sex Offender",
                   "sexually inappropriate": "Sexually Inappropriate",
                   "sodomized": "Sodom*",
                   "sodomy": "Sodom*",
                   "took advantage of her": "Took Advantage of",
                   "took advantage of me": "Took Advantage of"
                   }

def main():
    df = pd.read_csv("_cluster_rape_new_metadata.csv")
    report_table_df = pd.read_csv("hm_report_table.csv")

    keyword_to_files_dict = {}
    #For those with present birth decades
    all_women = 1785
    all_AA_women = 1097
    HM_women = 990

    women_totals = [all_women, all_AA_women, HM_women]

    for i, r in report_table_df.iterrows():
        keyword_to_files_dict[term_dictionary[r["keyword"].lower()]] = [[], [], []]

    #Get file counts for each keyword
    for i, r in df.iterrows():
        if pd.isnull(r["birth_decade"]) or r["birth_decade"] >= 1900 or r["researcher_assumed_birth_decade"] >= 1900:
            continue

        #All keywords
        if r["project_file_name"] not in keyword_to_files_dict["All"][0]: #All
            keyword_to_files_dict["All"][0].append(r["project_file_name"])

            if r["identified_race"] == "Black or African American" or r["researcher_assumed_race"] == "Black or African American" and\
                            r["project_file_name"] not in keyword_to_files_dict["All"][1]: #AA
                keyword_to_files_dict["All"][1].append(r["project_file_name"])

            if r["collection_id"] == "HM" and r["project_file_name"] not in keyword_to_files_dict["All"][2]: #HM
                keyword_to_files_dict["All"][2].append(r["project_file_name"])

        #Individual keywords
        if term_dictionary[r["keyword"].lower()] in keyword_to_files_dict.keys():
            if r["project_file_name"] not in keyword_to_files_dict[term_dictionary[r["keyword"].lower()]][0]: #All
                keyword_to_files_dict[term_dictionary[r["keyword"].lower()]][0].append(r["project_file_name"])

            if r["identified_race"] == "Black or African American" or r["researcher_assumed_race"] == "Black or African American" and\
                            r["project_file_name"] not in keyword_to_files_dict[term_dictionary[r["keyword"].lower()]][1]: #AA
                keyword_to_files_dict[term_dictionary[r["keyword"].lower()]][1].append(r["project_file_name"])

            if r["collection_id"] == "HM" and r["project_file_name"] not in keyword_to_files_dict[term_dictionary[r["keyword"].lower()]][2]: #HM
                keyword_to_files_dict[term_dictionary[r["keyword"].lower()]][2].append(r["project_file_name"])
        else:
            print("How?")

    #Generate the output list
    new_csv_list = list(keyword_to_files_dict.keys())
    new_csv_list.sort()

    for i in range(len(new_csv_list)):
        new_csv_list[i] = [new_csv_list[i]]
        for j in range(3):
            keyword_file_count = len(keyword_to_files_dict[new_csv_list[i][0]][j])
            new_csv_list[i].append(keyword_file_count)
            new_csv_list[i].append(round(100*keyword_file_count/women_totals[j], 2))

    new_csv_name = "birth_decade_keyword_count_and_percent_pre-1900.csv"
    new_csv_df = pd.DataFrame(new_csv_list)
    new_csv_df.to_csv(new_csv_name, index=False, header=new_csv_header)


if __name__ == '__main__':
    main()