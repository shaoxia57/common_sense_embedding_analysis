import pandas as pd

def filter_data_into_more_less_by_actual_comparison(result_data, param_data, option=0):
    if option == 1:
        premise = "asym_perturbs"
    else:
        premise = "premise"
    more = []
    less = []
    for i, row in result_data.iterrows():
        p_key = row["perturbation"] + "-" + row[premise]
        if param_data[str(row["truism_number"])]["greater_than"] == "A":
            if row["perturbation"] in ["original", "paraphrase", 
                                       "negation_antonym", "negation_paraphrase_inversion"]:
                if row[premise] == "original":
                    template_key = "more"
                else:
                    template_key = "less"
            else:
                if row[premise] == "original":
                    template_key = "less"
                else:
                    template_key = "more"
        else:
            if row["perturbation"] in ["original", "paraphrase", 
                                       "negation_antonym", "negation_paraphrase_inversion"]:
                if row[premise] == "original":
                    template_key = "less"
                else:
                    template_key = "more"
            else:
                if row[premise] == "original":
                    template_key = "more"
                else:
                    template_key = "less"

        if template_key == "more":
            more.append(row)
        else:
            less.append(row)

    return (pd.DataFrame.from_records(more), pd.DataFrame.from_records(less))


def filter_data_into_more_less_by_orig_comparison(result_data, param_data, option=0):
    if option:
        premise = "asym_perturbs"
        truism_number = "set_number"
    else:
        premise = "premise"
        truism_number = "truism_number"
    more = []
    less = []
    for i, row in result_data.iterrows():
        p_key = row["perturbation"] + "-" + row[premise]
        
        if param_data[str(row[truism_number])]["greater_than"] == "A":
            more.append(row)
        else:
            less.append(row)        

    return (pd.DataFrame.from_records(more), pd.DataFrame.from_records(less))

def get_perturbation_order(result_data, loop_count, option):
    if option == 1:
        premise = "asym_perturbs"
    else:
        premise = "premise"
    order = []
    for i, row in result_data.iterrows():
        p_key = row["perturbation"] + "-" + row[premise]
        order.append(p_key)
        if i >= loop_count-1:
            break
    
    return order

def transform_results_to_seperate_sql_dict(result_data, transformed_dict, stat_name, last_num, option, param_data=None):

    if option:
        premise = "asym_perturbs"
        truism_number = "set_number"
    else:
        premise = "premise"
        truism_number = "truism_number"


    for i, row in result_data.iterrows():
        if param_data:
            transformed_dict["template"].append(param_data[str(row[truism_number])]["template"])
        transformed_dict["set_number"].append(int(row[truism_number]) + last_num)
        transformed_dict["linguistic_operator"].append(row["perturbation"])
        transformed_dict["asymetric_operator"].append(row[premise])
        transformed_dict["stat"].append(row[stat_name])
    
    return transformed_dict

def transform_results_to_merged_sql_dict(result_data, transformed_dict, stat_name, last_num, option, param_data=None):

    if option:
        premise = "asym_perturbs"
        truism_number = "set_number"
    else:
        premise = "premise"
        truism_number = "truism_number"

    for i, row in result_data.iterrows():
        if param_data:
            transformed_dict["template"].append(param_data[str(row[truism_number])]["template"])
        transformed_dict["set_number"].append(int(row[truism_number]) + last_num)
        transformed_dict["perturbation"].append(row["perturbation"]+"-"+row[premise])
        transformed_dict["stat"].append(row[stat_name])
    
    return transformed_dict
