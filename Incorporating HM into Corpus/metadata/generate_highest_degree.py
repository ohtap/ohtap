import pandas as pd

output_csv_header = ["Accession#", "education"]

def has_grad_degree(degrees):
    grad_words = ["j.d", "m.s", "m.a", "m.p.a", "ph.d", "master",
                  "ed.d", "m.d", "m.p.h", "m.f.a", "a.m", "doctor",
                  "jd", "ms", "ma", "mpa", "phd", "edd", "md", "mph", "mfa",
                  "am", "sm", "s.m", "llm", "l.l.m", "ll.m", "llb", "l.l.b",
                  "s.b.t", "sbt", "law", "d.m", "mm", "m.m", "m.b.a", "mba",
                  "m.e.d", "med", "m.ed", "stm", "st.m", "mst", "m.st", "me.d",
                  "ll.b", "professional", "d.m", "dm", "dd", "d.d", "stb", "st.b",
                  "s.t.b", "mli", "m.l.i", "mpa", "m.p.a", "m.l.s", "mls", "m.s",
                  "msw", "ded", "d.ed"]

    for degree in degrees:
        for word in grad_words:
            if word in degree: return True

    return False

def has_bachelors_degree(degrees):
    bachelors_words = ["b.a", "b.a.e", "a.b", "b.s", "ba", "bs",
                       "sb", "ab", "bachelor", "b.ed", "bed", "bli", "b.l.i",
                       "bd", "b.d", "liberal arts", "bls", "b.l.s", "music",
                       "certificate", "architecture", "political", "engineering", "ed"]

    for degree in degrees:
        for word in bachelors_words:
            if word in degree: return True

    return False

def has_associates_degree(degrees):
    associates_words = ["associate", "aa", "a.a", "afa", "a.f.a", "aas", "a.a.s",
                        "as", "a.s"]

    for degree in degrees:
        for word in associates_words:
            if word in degree: return True

    return False

def has_some_college(schools):
    some_college_words = ["college", "university"]

    for school in schools:
        for word in some_college_words:
            if word in school: return True

    return False

def has_high_school_diploma(degrees):
    diploma_words = ["diploma", "dipolma", "hs", "h.s"]

    for degree in degrees:
        for word in diploma_words:
            if word in degree: return True

    return False

def has_some_high_school(schools):
    high_school_words = ["high school", "academy"]

    for school in schools:
        for word in high_school_words:
            if word in school: return True

    return False

def has_less_than_high_school(schools):
    any_school_words = ["elementary", "middle school"]

    for school in schools:
        for word in any_school_words:
            if word in school: return True

    return False

def get_highest_degree(schools, degrees):
    highest_degree = "Unknown"

    if has_grad_degree(degrees): highest_degree = "Graduate or professional degree"
    elif has_bachelors_degree(degrees): highest_degree = "Bachelor's degree"
    elif has_associates_degree(degrees): highest_degree = "Associate's degree"
    elif has_some_college(schools): highest_degree = "Some college"
    elif has_high_school_diploma(degrees): highest_degree = "High school graduate"
    elif has_some_high_school(schools): highest_degree = "9th to 12th grade but no diploma"
    elif has_less_than_high_school(schools): highest_degree = "Less than 9th grade"

    return highest_degree

def main():
    df = pd.read_csv("hm_degrees.csv")

    degree_list = []

    for i, row in df.iterrows():
        schools_and_degrees = row["Schools/Degrees"]
        schools = []
        degrees = []
        if isinstance(schools_and_degrees, str):
            schools_and_degrees = schools_and_degrees.split("$")
            #Generate lists of schools attended and degrees earned
            for school_and_degree in schools_and_degrees:
                split_pair = school_and_degree.split("-")
                if isinstance(split_pair[0], str):
                    schools.append(split_pair[0].lower().strip())

                if len(split_pair) > 1 and isinstance(split_pair[1], str):
                    degrees.append(split_pair[1].lower().strip())

        degree_list.append([row["Accession#"], get_highest_degree(schools, degrees)])

    degree_df = pd.DataFrame(degree_list)
    degree_df.to_csv("highest_degrees.csv", index=False, header=output_csv_header)


if __name__ == '__main__':
    main()