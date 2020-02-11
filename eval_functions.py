"""
    Functions used to evaluate the performance of a classifier

    Definitions:
        1. all      - Per label metric value.

        2. micro    - Performance across the whole dataset.
                      Will be the same across all metrics if all labels are used.
                      The micro measure in the above case will evaluate to the accuracy.
                      If you change which labels you would like to consider,
                      then the micros won't necessarily equal each other.

        3. macro    - The average of the per label value of the metric.

        4. weighted - The weighted, by frequency, average of the per label value of the metric.

    Some Notes:
        1. micro recall == accuracy no matter what labels are passed.
           In fact for every different definition of the metrics, recall
           equals the equivalent definition of accuracy.

        2. For now the get_roc_curve function can only be used for binary data

        3. Support represents the distribution of labels, and the number of
           labels in both the true labeling and predicted labeling passed in

    Useful Functions:
        1. get_all_metrics
        2. pretty_print_metrics
        3. plot_confusion_matrix
        4. plot_roc_curve
"""
import itertools
from collections import defaultdict, OrderedDict, Sequence
from sklearn.metrics import precision_score, recall_score, f1_score, \
                            auc, roc_curve, confusion_matrix
import numpy as np
import matplotlib.pyplot as plt

def get_precision_scores(y_true, y_predicted, labels=None):
    """
        Used to get the different definitions of precision

        Remember the binary definition of precision is of the positive class
        - you can get it by looking at the 2nd position of all array
            - assuming you are using 1 as pos_label

        Params:
            y_true      (arr) : true labeling of the data points
            y_predicted (arr) : predicted labeling of the data points
            labels      (arr) : labels to consider when calculating values

        Returns:
            OrderedDict : key   - definition type
                          value - precision as per the definition type
    """
    #pylint: disable=too-many-boolean-expressions, len-as-condition
    if ((isinstance(labels, (Sequence, np.ndarray)) and len(labels)) or labels is None) and \
       (isinstance(y_true, (Sequence, np.ndarray)) and len(y_true)) and \
       (isinstance(y_predicted, (Sequence, np.ndarray)) and len(y_predicted)):
        try:
            micro = precision_score(y_true, y_predicted, labels=labels, average='micro')
            macro = precision_score(y_true, y_predicted, labels=labels, average='macro')
            weighted = precision_score(y_true, y_predicted, labels=labels, average='weighted')
            all_classes = precision_score(y_true, y_predicted, labels=labels, average=None)
            all_classes = [float(x) for x in all_classes]

            return OrderedDict([("all", all_classes),
                                ("micro", micro),
                                ("macro", macro),
                                ("weighted", weighted)])
        except:
            raise Exception("Error happened at Precision Call:\n \
                             Please send in the following parameters:\n \
                             1. true labels of the data (array like)\n \
                             2. result of the classifier's predict function\n \
                             3. labels - None (default), labels you would like to consider")
    else:
        raise ValueError("y_true must be a non empty array like \n \
                          y_predicted must be a non empty array like \n \
                          labels must either be None or a non empty array like")


def get_recall_scores(y_true, y_predicted, labels=None):
    """
        Used to get the different definitions of recall

        Remember the binary definition of recall is of the positive class
        - you can get it by looking at the 2nd position of all array
            - assuming you are using 1 as pos_label

        Params:
            y_true      (arr) : true labeling of the data points
            y_predicted (arr) : predicted labeling of the data points
            labels      (arr) : labels to consider when calculating values

        Returns:
            OrderedDict : key   - definition type
                          value - recall as per the definition type
    """
    #pylint: disable=too-many-boolean-expressions, len-as-condition
    if ((isinstance(labels, (Sequence, np.ndarray)) and len(labels)) or labels is None) and \
       (isinstance(y_true, (Sequence, np.ndarray)) and len(y_true)) and \
       (isinstance(y_predicted, (Sequence, np.ndarray)) and len(y_predicted)):
        try:
            micro = recall_score(y_true, y_predicted, labels=labels, average='micro')
            macro = recall_score(y_true, y_predicted, labels=labels, average='macro')
            weighted = recall_score(y_true, y_predicted, labels=labels, average='weighted')
            all_classes = recall_score(y_true, y_predicted, labels=labels, average=None)
            all_classes = [float(x) for x in all_classes]

            return OrderedDict([("all", all_classes),
                                ("micro", micro),
                                ("macro", macro),
                                ("weighted", weighted)])
        except:
            raise Exception("Error happened at Recall Call:\n \
                             Please send in the following parameters:\n \
                             1. true labels of the data (array like)\n \
                             2. result of the classifier's predict function\n \
                             3. labels - None (default), labels you would like to consider")
    else:
        raise ValueError("y_true must be a non empty array like \n \
                          y_predicted must be a non empty array like \n \
                          labels must either be None or a non empty array like")


def get_f1_scores(y_true, y_predicted, labels=None):
    """
        Used to get the different definitions of f1

        Remember the binary definition of f1 is of the positive class
        - you can get it by looking at the 2nd position of all array
            - assuming you are using 1 as pos_label

        Params:
            y_true      (arr) : true labeling of the data points
            y_predicted (arr) : predicted labeling of the data points
            labels      (arr) : labels to consider when calculating values

        Returns:
            OrderedDict : key   - definition type
                          value - f1 as per the definition type
    """
    #pylint: disable=too-many-boolean-expressions, len-as-condition
    if ((isinstance(labels, (Sequence, np.ndarray)) and len(labels)) or labels is None) and \
       (isinstance(y_true, (Sequence, np.ndarray)) and len(y_true)) and \
       (isinstance(y_predicted, (Sequence, np.ndarray)) and len(y_predicted)):
        try:
            micro = f1_score(y_true, y_predicted, labels=labels, average='micro')
            macro = f1_score(y_true, y_predicted, labels=labels, average='macro')
            weighted = f1_score(y_true, y_predicted, labels=labels, average='weighted')
            all_classes = f1_score(y_true, y_predicted, labels=labels, average=None)
            all_classes = [float(x) for x in all_classes]

            return OrderedDict([("all", all_classes),
                                ("micro", micro),
                                ("macro", macro),
                                ("weighted", weighted)])
        except:
            raise Exception("Error happened at F1 Call:\n \
                             Please send in the following parameters:\n \
                             1. true labels of the data (array like)\n \
                             2. result of the classifier's predict function\n \
                             3. labels - None (default), labels you would like to consider")
    else:
        raise ValueError("y_true must be a non empty array like \n \
                          y_predicted must be a non empty array like \n \
                          labels must either be None or a non empty array like")


def get_distribution(y_true, y_predicted, labels=None):
    """
        Gets the distributions for y_true and y_predicted

        For both y_true and y_predicted, we get the distribution and count
        for the arrays
            - the counts can differ if you change what labels to consider

        Params:
            y_true      (arr) : true labeling of the data points
            y_predicted (arr) : predicted labeling of the data points
            labels      (arr) : labels to consider when calculating values

        Returns:
            OrderedDict : key   - arrayName_(dist|count)
                          value - dist or count for that array
    """
    #pylint: disable=len-as-condition
    if labels is None or len(labels):
        try:
            labels_to_check = None
            if labels:
                labels_to_check = labels
            else:
                labels_to_check = set(y_true)

            y_true_dist = defaultdict(int)
            true_count = 0.0
            for label in y_true:
                if label in labels_to_check:
                    y_true_dist[label] += 1
                    true_count += 1

            y_true_dist = [value/true_count for key, value in \
                            sorted(y_true_dist.items())]

            y_predicted_dist = defaultdict(int)
            pred_count = 0.0
            for label in y_predicted:
                if label in labels_to_check:
                    y_predicted_dist[label] += 1
                    pred_count += 1

            y_predicted_dist = [value/pred_count for key, value in \
                                sorted(y_predicted_dist.items())]

            return OrderedDict([("y_true_dist", np.array(y_true_dist)),
                                ("y_true_count", true_count),
                                ("y_predicted_dist", np.array(y_predicted_dist)),
                                ("y_predicted_count", pred_count)])
        except:
            raise Exception("Error happened at Precision Call:\n \
                             Please send in the following parameters:\n \
                             1. true labels of the data (array like)\n \
                             2. result of the classifier's predict function\n \
                             3. labels - None (default), labels you would like to consider")
    else:
        raise ValueError("labels must either be None or a non empty array")


def get_all_metrics(y_true, y_predicted, labels=None):
    """
        Calculates precision, recall, f1, support, confusion_matrix and
        accuracy for a classifier's performance.
        For each metric the function calculates the metric using the above
        4 definitions.

        Params:
            y_true      (arr) : true labeling of the data points
            y_predicted (arr) : predicted labeling of the data points
            labels      (arr) : labels to consider when calculating values

        Returns:
            OrderedDict : key   - metric type
                          value - OrderedDict where key-value pairs represent
                                  definition_type - definition_value
    """
    #pylint: disable=too-many-boolean-expressions, len-as-condition
    if ((isinstance(labels, (Sequence, np.ndarray)) and len(labels)) or labels is None) and \
       (isinstance(y_true, (Sequence, np.ndarray)) and len(y_true)) and \
       (isinstance(y_predicted, (Sequence, np.ndarray)) and len(y_predicted)):
        try:
            precision = get_precision_scores(y_true, y_predicted, labels)

            recall = get_recall_scores(y_true, y_predicted, labels)

            f1_measure = get_f1_scores(y_true, y_predicted, labels)

            support = get_distribution(y_true, y_predicted, labels)

            cm = confusion_matrix(y_true, y_predicted, labels=labels)
            
            cm = cm.astype('float') / cm.sum(axis=1)[:, np.newaxis]

            accuracy = recall["micro"]

            return OrderedDict([("accuracy", accuracy),
                                ("precision", precision),
                                ("recall", recall),
                                ("f1_measure", f1_measure),
                                ("support", support),
                                ("confusion_matrix", cm)])
        except:
            raise Exception("Please send in the following parameters:\n \
                             1. true labels of the data (array like)\n \
                             2. result of the classifier's predict function\n \
                             3. labels - None (default), labels you would like to consider")
    else:
        raise ValueError("y_true must be a non empty array like \n \
                          y_predicted must be a non empty array like \n \
                          labels must either be None or a non empty array like")

def average_all_metrics(y_true_array, y_predicted_array, n_labels):

    metrics = {
        "accuracy" : 0,
        "precision" : {"all" : [0] * n_labels, "micro" : 0, "macro" : 0, "weighted" : 0},
        "recall" : {"all" : [0] * n_labels, "micro" : 0, "macro" : 0, "weighted" : 0},
        "f1_measure" : {"all" : [0] * n_labels, "micro" : 0, "macro" : 0, "weighted" : 0},
        "support" : {"y_true_dist" : [0] * n_labels, "y_true_count" : 0, "y_predicted_dist" : [0] * n_labels, "y_predicted_count" : 0},
        "confusion_matrix" : [[0 for x in range(n_labels)] for y in range(n_labels)] 
    }

    not_sub_keys = ["confusion_matrix", "accuracy"]
    arrays = ["all", "y_true_dist", "y_predicted_dist"]

    for i, y_true in enumerate(y_true_array):
        y_predicted = y_predicted_array[i]
        metric = get_all_metrics(y_true, y_predicted)
        for key in metric:
            if key not in not_sub_keys:
                for sub_key in metric[key]:
                    if sub_key not in arrays:
                        metrics[key][sub_key] += metric[key][sub_key]
                    else:
                        for i, entry in enumerate(metric[key][sub_key]):
                            metrics[key][sub_key][i] += entry
            else:
                if key == "accuracy":
                    metrics["accuracy"] += metric["accuracy"]
                else:
                    for i, row in enumerate(metric["confusion_matrix"]):
                        for j, value in enumerate(metric["confusion_matrix"][i]):
                            metrics["confusion_matrix"][i][j] += value

    number_of_iters = float(len(y_true_array))

    for key in metrics:
        if key not in not_sub_keys:
            for sub_key in metrics[key]:
                if sub_key not in arrays:
                    metrics[key][sub_key] = metrics[key][sub_key] / number_of_iters
                else:
                    for i, entry in enumerate(metric[key][sub_key]):
                        metrics[key][sub_key][i] = metrics[key][sub_key][i] / number_of_iters
        else:
            if key == "accuracy":
                metrics["accuracy"] = metrics["accuracy"] / number_of_iters
            else:
                for i, row in enumerate(metrics["confusion_matrix"]):
                        for j, value in enumerate(metrics["confusion_matrix"][i]):
                            metrics["confusion_matrix"][i][j] = value / number_of_iters
    
    metrics["confusion_matrix"] = np.array(metrics["confusion_matrix"]).astype('float') / np.array(metrics["confusion_matrix"]).sum(axis=1)[:, np.newaxis]

    return OrderedDict([("iterations", number_of_iters),
                        ("accuracy", metrics["accuracy"]),
                        ("precision", metrics["precision"]),
                        ("recall", metrics["recall"]),
                        ("f1_measure", metrics["f1_measure"]),
                        ("support", metrics["support"]),
                        ("confusion_matrix", metrics["confusion_matrix"])])

def pretty_print_metrics(metrics):
    """
        Creates an easy to read string representation of the OrderedDict of
        metric values outputted by the above get_all_metrics function.

        Params:
            metrics : OrderedDict outputted by get_all_metrics()

        Returns:
            str : easy to read string representation of the input
    """
    try:
        not_print = ["confusion_matrix", "accuracy", "iterations"]
        arrays = ["all", "y_true_dist", "y_predicted_dist"]
        output = "iterations: " + str(int(metrics["iterations"])) if  "iterations" in metrics else "1"
        output += "\n\n"
        output += "accuracy: " + "%.3f" % metrics["accuracy"]
        output += "\n\n"
        for key in metrics:
            if key not in not_print:
                formatted_key = key + ": "
                output += formatted_key
                output += "\n"
                output += "\t"
                for entry in metrics[key]:
                    formatted_entry = entry + ": "
                    output += formatted_entry
                    if entry in arrays:
                        output += str(["%.3f" % x for x in metrics[key][entry]])
                    else:
                        output += "%.3f" % metrics[key][entry]
                    output += "\n"
                    output += "\t"

                output += "\n"

        return output
    except:
        raise Exception("Please send in the results of get_all_metrics()")


def plot_roc_curve(y_true, y_pred_scores, pos_label=1):
    """
        Creates an ROC graph for a given array of true labels and predicted
        scores

        You can send in a different label if needed for the positive label in
        your data
        Only works on BINARY data

        Params:
            y_true          (arr) : true labeling of the data points
            y_pred_scores   (arr) : array of scores as to how likely a given
                                    point is of the positive class
            pos_label       (int) : the label associated with what the
                                    classifier deems the positive class
    """
    #pylint: disable=unused-variable, len-as-condition
    fpr, tpr, tresh = roc_curve(y_true, y_pred_scores, pos_label=pos_label)
    area = auc(fpr, tpr)
    plt.figure()
    line_width = 2
    plt.plot(fpr, tpr, color='darkorange', lw=line_width,
             label='ROC curve (area = %0.2f)' % area)
    plt.plot([0, 1], [0, 1], color='navy', lw=line_width, linestyle='--')
    plt.xlim([0.0, 1.0])
    plt.ylim([0.0, 1.05])
    plt.xlabel('False Positive Rate')
    plt.ylabel('True Positive Rate')
    plt.title('Receiver operating characteristic')
    plt.legend(loc="lower right")
    plt.show()


#pylint: disable=invalid-name,no-member
def plot_confusion_matrix(cm, classes=None, normalize=True, small=False,
                          title='Confusion matrix', cmap=plt.cm.Blues):
    # pylint: disable=line-too-long
    """
    This function prints and plots the confusion matrix.
    Normalization can be applied by setting normalize=True.
    Taken from : http://scikit-learn.org/stable/auto_examples/model_selection/plot_confusion_matrix.html#sphx-glr-auto-examples-model-selection-plot-confusion-matrix-py
    Params:
        cm              (arr) : the confusion matrix to plot
        classes         (arr) : the various class labels
        normalize      (bool) : to normalize the probabilities or not
        title           (str) : title of plot
        cmap  (matplotlib.cm) : the color scheme to use for the confusion
                                matrix
    """
    if not classes:
        classes = [str(i) for i in range(len(cm))]

    if normalize:
        cm = cm.astype('float') / cm.sum(axis=1)[:, np.newaxis]

    if not small:
        plt.figure(num=1, figsize=(20, 15))
    else:
        plt.figure()
    plt.imshow(cm, interpolation='nearest', cmap=cmap)
    plt.title(title)
    plt.colorbar()
    tick_marks = np.arange(len(classes))
    plt.xticks(tick_marks, classes)
    plt.yticks(tick_marks, classes)

    fmt = '.2f' if normalize else 'd'
    thresh = cm.max() / 2.
    for i, j in itertools.product(range(cm.shape[0]), range(cm.shape[1])):
        plt.text(j, i, format(cm[i, j], fmt),
                 horizontalalignment="center",
                 color="white" if cm[i, j] > thresh else "black")

    plt.tight_layout()
    plt.ylabel('True Masked Word')
    plt.xlabel('Guessed Masked Word')
    plt.show()


def average_feature_importances(feature_importances_array):
    final_feature_importances = [0] * len(feature_importances_array[0])
    for i, row in enumerate(feature_importances_array):
        for j, feature in enumerate(row):
            final_feature_importances[j] += feature

    iter_length = float(len(feature_importances_array))
    for i, feature_sum in enumerate(final_feature_importances):
        final_feature_importances[i] = feature_sum/float(iter_length)

    return final_feature_importances


