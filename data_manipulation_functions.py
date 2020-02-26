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

def transform_results_to_seperate_sql_dict(result_data, param_data, transformed_dict, stat_name, last_num, option):

    if option:
        premise = "asym_perturbs"
        truism_number = "set_number"
    else:
        premise = "premise"
        truism_number = "truism_number"


    for i, row in result_data.iterrows():
        transformed_dict["template"].append(param_data[str(row[truism_number])]["template"])
        transformed_dict["set_number"].append(int(row[truism_number]) + last_num)
        transformed_dict["linguistic_operator"].append(row["perturbation"])
        transformed_dict["asymetric_operator"].append(row[premise])
        transformed_dict["stat"].append(row[stat_name])
    
    return transformed_dict

def transform_results_to_merged_sql_dict(result_data, param_data, transformed_dict, stat_name, last_num, option):

    if option:
        premise = "asym_perturbs"
        truism_number = "set_number"
    else:
        premise = "premise"
        truism_number = "truism_number"

    for i, row in result_data.iterrows():
        transformed_dict["template"].append(param_data[str(row[truism_number])]["template"])
        transformed_dict["set_number"].append(int(row[truism_number]) + last_num)
        transformed_dict["perturbation"].append(row["perturbation"]+"-"+row[premise])
        transformed_dict["stat"].append(row[stat_name])
    
    return transformed_dict