import pandas as pd
import copy

new_csv_header = ["keyword"]

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
    interviewees_df = pd.read_csv("interviewees.csv")

    keyword_to_files_dict = {}
    #For those with present birth decades

    #Count the number of women in each collection
    collection_women_totals = {"All": 0}
    interviewees_list = []

    for i, r in interviewees_df.iterrows():
        if r["sex"] == "Male" or r["interviewee_name"] in interviewees_list:
            continue

        collection_women_totals["All"] += 1
        if collection_women_totals.get(r["collection_id"]) is None:
            collection_women_totals[r["collection_id"]] = 1
        else:
            collection_women_totals[r["collection_id"]] += 1

    #Create the dictionary of collections to counts for each term grouping
    collection_term_totals= {}
    for new_key in collection_women_totals.keys():
        collection_term_totals[new_key] = []
    for i, r in report_table_df.iterrows():
        keyword_to_files_dict[term_dictionary[r["keyword"].lower()]] = copy.deepcopy(collection_term_totals)


    #Data structure is: Dict of keywords, to dict of collections to list of file names
    #Get file counts for each keyword
    for i, r in df.iterrows():
        #All keywords
        if r["project_file_name"] not in keyword_to_files_dict["All"]["All"]: #All terms, All collections
            keyword_to_files_dict["All"]["All"].append(r["project_file_name"])

            keyword_to_files_dict["All"][r["collection_id"]].append(["project_file_name"]) #All terms, Specific collection

        #Individual keywords
        if term_dictionary[r["keyword"].lower()] in keyword_to_files_dict.keys():
            if r["project_file_name"] not in keyword_to_files_dict[term_dictionary[r["keyword"].lower()]]["All"]: #Specific term, All collections
                keyword_to_files_dict[term_dictionary[r["keyword"].lower()]]["All"].append(r["project_file_name"])

                if r["project_file_name"] not in keyword_to_files_dict[term_dictionary[r["keyword"].lower()]][r["collection_id"]]:
                    keyword_to_files_dict[term_dictionary[r["keyword"].lower()]][r["collection_id"]].append(r["project_file_name"]) #Specific term, Specific collection

        else:
            print("How?")

    collection_name_list = list(collection_term_totals.keys())
    collection_name_list.sort()

    #Create the new_csv_header
    for collection_name in collection_name_list:
        new_csv_header.append(collection_name + " N")
        new_csv_header.append(collection_name + " %")

    # Generate the output list
    new_csv_list = list(keyword_to_files_dict.keys())
    new_csv_list.sort()

    for i in range(len(new_csv_list)):
        current_keyword = new_csv_list[i]
        new_csv_list[i] = [new_csv_list[i]]
        for j in range(len(collection_name_list)):
            keyword_file_count = len(keyword_to_files_dict[current_keyword][collection_name_list[j]])
            #keyword_file_count = len(keyword_to_files_dict[new_csv_list[i][0]]["All"][collection_name_list[j]])
            new_csv_list[i].append(keyword_file_count)
            new_csv_list[i].append(round(100*keyword_file_count/collection_women_totals[collection_name_list[j]], 2))

    new_csv_name = "keyword_count_and_percent_by_collection.csv"
    new_csv_df = pd.DataFrame(new_csv_list)
    new_csv_df.to_csv(new_csv_name, index=False, header=new_csv_header)


if __name__ == '__main__':
    main()