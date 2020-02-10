def get_templates(param_array):
    templates = {}
    for param_dict in param_array:
        for key in param_dict:
            templates[param_dict[key]["template"]] = {}
    return templates

def get_perturbations(result_data, template_dict):
#     print(result_data)
    for i, row in result_data.iterrows():
#         print(row)
        p_key = row["perturbation"] + "-" + row["premise"]
#         print(p_key)
        for key in template_dict:
            template_dict[key][p_key] = {"accuracy" : 0, "ratio_score" : 0}
    return template_dict

def get_perturbation_order(result_data, loop_count):
    order = []
    for i, row in result_data.iterrows():
        p_key = row["perturbation"] + "-" + row["premise"]
        order.append(p_key)
        if i >= loop_count-1:
            break
    
    return order

def fill_pertubation_data(result_data, param_data, template_dict, multiple=1):
    completed_truisms = {}
    
    for i, row in result_data.iterrows():
        p_key = row["perturbation"] + "-" + row["premise"]
        template_key = param_data[str(row["truism_number"])]["template"]
        
        template_dict[template_key][p_key]["accuracy"] += row["avg_binary_score"]*multiple
        template_dict[template_key][p_key]["ratio_score"] += row["avg_ratio_score"]*multiple
        
        if row["truism_number"] not in completed_truisms:
            template_dict[template_key]["count"] += 1*multiple
            completed_truisms[row["truism_number"]] = 1

    return template_dict

def create_tables(averaged_numbers, perturbation_order, threshold):
    output = {}
    output_2 = {}
    sorted_keys = list(averaged_numbers.keys())
    sorted_keys.sort()
    for template in sorted_keys:
        for perturbation in perturbation_order:
            if perturbation in output:
                output[perturbation].append(averaged_numbers[template][perturbation])
                if averaged_numbers[template][perturbation] <= threshold:
                    output_2[perturbation].append("X")
                else:
                    output_2[perturbation].append("O")
            else:
                output[perturbation] = []
                output_2[perturbation] = []
                output[perturbation].append(averaged_numbers[template][perturbation])
                if averaged_numbers[template][perturbation] <= threshold:
                    output_2[perturbation].append("X")
                else:
                    output_2[perturbation].append("O")
    
    return (pd.DataFrame.from_dict(output), pd.DataFrame.from_dict(output_2))

def aggregate_pertubations(raw_template_data, metric):
    total_count = 0.0
    for template in raw_template_data:
        total_count += raw_template_data[template]["count"]
    
    one_key = list(raw_template_data.keys())[0]
    
    output = {}
    for perturbation in raw_template_data[one_key]:
        if perturbation != "count":
            for template in raw_template_data:
                if perturbation in output:
                    output[perturbation] += raw_template_data[template][perturbation][metric]
                else:
                    output[perturbation] = raw_template_data[template][perturbation][metric]
    
    for key in output:
        output[key] = output[key] / total_count
    
    return output

def aggregate_templates(raw_template_data, metric):   
    output = {}
    for template in raw_template_data:
        output[template] = {"count" : 0, "pct" : -1, "total" : -1}
        for perturbation in raw_template_data[template]:
            if perturbation != "count":
#                 if template in output:
                output[template]["count"] += raw_template_data[template][perturbation][metric]
#                 else:
#                     output[template] = raw_template_data[template][perturbation][metric]
    
    for key in output:
        output[key]["total"] = float((len(raw_template_data[key].keys()) - 1) * raw_template_data[key]["count"])
        output[key]["pct"] = output[key]["count"] / output[key]["total"]
    
    return output

def autolabel(rects, ax, below, color):
    """Attach a text label above each bar in *rects*, displaying its height."""
    for rect in rects:
        height = rect.get_height()
        if below:
            y = min(-0.2, -2*height)
            va = "bottom"
            x = rect.get_x() + 4*rect.get_width() / 5
        else:
            y = height * 1.05
            x = rect.get_x() + rect.get_width() / 2
            va = "bottom"
            
        ax.annotate('{}'.format(height),
                    xy=(x, y),
                    xytext=(0, 3),  # 3 points vertical offset
                    textcoords="offset points",
                    ha='center', va=va, color=color, weight='bold')

def display_two_axis_bar_plot(x_labels, x_label, left_units, right_units, 
                              left_bar_data, right_bar_data, title, save=False):
    
    # https://matplotlib.org/gallery/api/two_scales.html
    
    # https://matplotlib.org/gallery/lines_bars_and_markers/barchart.html#sphx-glr-gallery-lines-bars-and-markers-barchart-py
    fig, ax1 = plt.subplots()
    x = np.arange(len(x_labels))
    width = 0.35
    
    color = 'tab:red'
    ax1.set_ylabel(left_units, color=color)
    ax1.set_ylim(bottom=0)
    rects1 = ax1.bar(x - width/2, left_bar_data, width, label=left_units, color=color)
    ax1.tick_params(axis='y', labelcolor=color)
    ax1.set_xticks(x)
    ax1.set_xticklabels(x_labels)
    ax1.set_xlabel(x_label)
    
    ax2 = ax1.twinx()  # instantiate a second axes that shares the same x-axis
    color = 'tab:blue'
    ax2.set_ylabel(right_units, color=color)
    ax2.set_ylim(bottom=-1, top=1)
    rects2 = ax2.bar(x + width/2, right_bar_data, width, label=right_units, color=color)
    ax2.tick_params(axis='y', labelcolor=color)
    
    ax1.legend(loc=2)
    ax2.legend(loc=0)
    
    autolabel(rects1, ax1, False, "tab:red")
    autolabel(rects2, ax2, True, "tab:blue")
    
    ax1.set_title(title)
    
    fig.tight_layout()  # otherwise the right y-label is slightly clipped
    if save:
        plt.savefig("{}.png".format(title))
    
    plt.show()