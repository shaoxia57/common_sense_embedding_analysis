import matplotlib.pyplot as plt
import matplotlib
import pandas as pd
import numpy as np

def create_table(grouped_numbers, columns_in_order, column_name, stat):
    output = {}
    for column in columns_in_order:
        output[column] = []
    
    for i, row in grouped_numbers.iterrows():
        output[row[column_name]].append(row[stat])
    
    return pd.DataFrame.from_dict(output)

def autolabel(rects, ax, color, below=False):
    """Attach a text label above each bar in *rects*, displaying its height."""
    for rect in rects:
        height = rect.get_height()
        bottom = below
        
        if height < 0:
            bottom = True
        
        if bottom:
            # multiple = 1.1 if height < 0 else -1.1
            # y = min(-0.15, multiple*height)
            # y = height 
            y = -0.2
            va = "bottom"
            x = rect.get_x() + rect.get_width() / 2
        else:
            if 0.33 - height < 0.05:
                y = height * 1.13
            else:
                y = height

            # y = 0.55
            x = rect.get_x() + rect.get_width() / 2
            va = "bottom"

        ax.annotate('{}'.format(height),
                    xy=(x, y),
                    xytext=(0, 3),  # 3 points vertical offset
                    textcoords="offset points",
                    ha='center', va=va, color=color, fontsize=8, weight='bold')

def display_two_axis_bar_plot(x_labels, x_label, left_units, right_units, 
                              left_bar_data, right_bar_data, title, save_dir="",
                              legend_loc=1, label_x_ticks=True, x_ticks_rotation=15,
                              add_nums_to_bars=True, nums_should_be_below=[False, True],
                              left_range=[0,1], right_range=[-1,1], small_title=False,
                              rand=None):
    
    # https://matplotlib.org/gallery/api/two_scales.html
    
    # https://matplotlib.org/gallery/lines_bars_and_markers/barchart.html#sphx-glr-gallery-lines-bars-and-markers-barchart-py
    fig, ax1 = plt.subplots()
    x = np.arange(len(x_labels))
    width = 0.35
    if rand:
        rand_level=rand
    else:
        rand_level=sum(left_range)/2.0
    
    color = 'tab:red'
    ax1.set_ylabel(left_units, color=color)
    ax1.set_ylim(bottom=left_range[0], top=left_range[1])
    rects1 = ax1.bar(x - width/2, left_bar_data, width, color=color)
    ax1.tick_params(axis='y', labelcolor=color)
    ax1.set_xticks(x)
    
    if label_x_ticks:
        ax1.set_xticklabels(x_labels, rotation=x_ticks_rotation)
    
    ax1.set_xlabel(x_label)
    
    ax2 = ax1.twinx()  # instantiate a second axes that shares the same x-axis
    color = 'tab:blue'
    ax2.set_ylabel(right_units, color=color)
    ax2.set_ylim(bottom=right_range[0], top=right_range[1])
    rects2 = ax2.bar(x + width/2, right_bar_data, width, color=color)
    ax2.tick_params(axis='y', labelcolor=color)
    
    if add_nums_to_bars:
        autolabel(rects1, ax1, "tab:red", nums_should_be_below[0])
        autolabel(rects2, ax2, "tab:blue", nums_should_be_below[1])
    
    if small_title:
        ax1.set_title(title, size=10)

    if small_title:
        ax1.set_title(title, size=10)
    else:
        ax1.set_title(title)

    random_guess = ax1.axhline(y=rand_level,color="darkgray", linestyle=":") 
    ax1.legend((rects1, rects2, random_guess), (left_units, right_units, "Random Guess"),
               loc=legend_loc, ncol=1, fontsize=10, framealpha=0.8)
    
    fig.tight_layout()  # otherwise the right y-label is slightly clipped
    if len(save_dir):
        plt.savefig("{}{}.pdf".format(save_dir, title), format='pdf', dpi=1200)
    
    plt.show()

def display_two_bar_plot(x_labels, x_label, y_label, y_one_label, y_two_label, data_one,
                         data_two, title, save_dir="", legend_loc=1, label_x_ticks=True, x_ticks_rotation=15,
                         add_nums_to_bars=True, nums_should_be_below=[False, True], y_range=[0,1], small_title=False,
                         rand=None):
    
    # https://matplotlib.org/gallery/api/two_scales.html
    
    # https://matplotlib.org/gallery/lines_bars_and_markers/barchart.html#sphx-glr-gallery-lines-bars-and-markers-barchart-py
    fig, ax1 = plt.subplots()
    x = np.arange(len(x_labels))
    width = 0.35

    if rand:
        rand_level=rand
    else:
        rand_level=sum(y_range)/2.0
    
    color_1 = 'tab:red'
    color_2 = 'tab:blue'
    ax1.set_ylabel(y_label, color=color_1)
    ax1.set_ylim(bottom=y_range[0], top=y_range[1])
    rects1 = ax1.bar(x - width/2, data_one, width, color=color_1)
    rects2 = ax1.bar(x + width/2, data_two, width, color=color_2)
    ax1.tick_params(axis='y', labelcolor=color_1)
    ax1.set_xticks(x)
    
    if label_x_ticks:
        ax1.set_xticklabels(x_labels, rotation=x_ticks_rotation)
    
    ax1.set_xlabel(x_label)
    
    if add_nums_to_bars:
        autolabel(rects1, ax1, color_1, nums_should_be_below[0])
        autolabel(rects2, ax1, color_2, nums_should_be_below[0])
    
    random_guess = ax1.axhline(y=rand_level, color='silver', linestyle=":")    
    
    if small_title:
        ax1.set_title(title, size=10)
    else:
        ax1.set_title(title)

    ax1.legend((rects1, rects2, random_guess), (y_one_label, y_two_label, "Random Guess"),
               loc=legend_loc, ncol=1, fontsize=10, framealpha=0.8)
    
    fig.tight_layout()  # otherwise the right y-label is slightly clipped
    ax1.set_title(title, size=10)
    if len(save_dir):
        plt.savefig("{}{}.pdf".format(save_dir, title), format='pdf', dpi=1200)
    
    plt.show()

def display_bar_plot(x_labels, x_label, y_label, data, title, color, save_dir="", legend_loc=1, label_x_ticks=True,
                     x_ticks_rotation=15, add_nums_to_bars=True, nums_should_be_below=False, y_range=[0,1], small_title=False,
                     rand=None):
    
    # https://matplotlib.org/gallery/api/two_scales.html
    
    # https://matplotlib.org/gallery/lines_bars_and_markers/barchart.html#sphx-glr-gallery-lines-bars-and-markers-barchart-py
    fig, ax1 = plt.subplots()
    if type(x_labels) == type([]):
        x = np.arange(len(x_labels))
    else:
        x = np.arange(x_labels[0], x_labels[1], 1)
    width = 0.35

    if rand:
        rand_level=rand
    else:
        rand_level=sum(y_range)/2.0
    
    ax1.set_ylabel(y_label, color=color)
    ax1.set_ylim(bottom=y_range[0], top=y_range[1])

    rects1 = ax1.bar(x, data, width, label=y_label, color=color)
    ax1.tick_params(axis='y', labelcolor=color)

    if type(x_labels) == type([]):
        if label_x_ticks:
            ax1.set_xticks(x)
            ax1.set_xticklabels(x_labels, rotation=x_ticks_rotation)
    else:
        ax1.set_xlim(x_labels[0], x_labels[1])
    
    ax1.set_xlabel(x_label)

    if add_nums_to_bars:
        autolabel(rects1, ax1, color, nums_should_be_below)

    random_guess = ax1.axhline(y=rand_level,color='silver', linestyle=":")    
    
    if small_title:
        ax1.set_title(title, size=10)
    else:
        ax1.set_title(title)

    ax1.legend((rects1, random_guess), (y_label, "Random Guess"), loc=legend_loc, ncol=1, fontsize=10, framealpha=0.8)
    
    fig.tight_layout()  # otherwise the right y-label is slightly clipped
    if len(save_dir):
        plt.savefig("{}{}.pdf".format(save_dir, title), format='pdf', dpi=1200)
    
    plt.show()