### Repo Dedicated To Investigating and Improving the Common Sense Reasoning Ability of Neural Lanugage Models

### Layout:
* data - all inputs and outputs used in scripts or notebooks live here. We currently have three evaluation settings: entailment, generation, masked-word-prediction. For each of these three settings we have dedicated folders for the following three stages of our investigation/evaluation pipeline:
    - Raw Data:
        + Entailment: truism_data + `prepare_sentence_pair` in `dataset_creation/pre_processing_utils.py`
        + Generation: truism_data + `prepare_truism_data_for_sentence_scoring` in `dataset_creation/pre_processing_utils.py` (but also stored in generation_test_data)
        + Masked Word Prediction: truism_data + `prepare_masked_instances` in `dataset_creation/pre_processing_utils.py`
    - Result Of Experiments Data:
        + Entailment: entailment_result_data
        + Generation: generation_result_data
        + Masked Word Prediction: masked_word_result_data
    - Visuals + Analysis of Data:
        + Entailment: analyzed_entailment_data
        + Generation: analyzed_generation_data
        + Masked Word Prediction: analyzed_masked_word_data

* dataset_creation - all notebooks and code to do with the creation of datasets
* experiment_utils - all notebooks and code to with the running of experiments
* evaluation_utils - all notebooks and code to with the evaluation of experiments
