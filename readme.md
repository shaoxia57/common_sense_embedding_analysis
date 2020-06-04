### Repo Dedicated To Investigating and Improving the Common Sense Reasoning Ability of Neural Lanugage Models

### Installation Instructions:
1. install python 3.6.5
2. create a virtual environmnet (`python3.6.5 -m venv your_virtual_env`)
3. `pip install -r rqs.txt`
4. Make sure you do a recursive git pull (if applicable), `git submodule update --init --recursive`, `git submodule update --recursive`

Additionaly to run COMET trials:

1. Download models from https://drive.google.com/open?id=1OidJPclQ5VoK6hBeLV52wBIg1OAw1tOH
2. `cd dataset_creation/kb_crawl`
3. unzip downloaded file here

### Experiment Running Instructions:
1. All evaluation experiments can be found in `experiment_utils`
2. Running **NON-COMET**  evaluation experiments must be done within the `experiment_utils` folder
    * Example: `python run_entailment_roberta_eval.py`
3. All **COMET** experiments must be done from the root of this repo and you must go to `dataset_creation/pre_processing_utils.py` and uncomment the line 10's import statement
    * Example: `python experiment_utils/run_generative_comet_atmoic.py`
4. Our fine-tuning scripts are based on a fork of the [HappyTransformer](https://github.com/EricFillion/happy-transformer) Project, `happy-transformer`. An example of how to use our fork can be found here:
    * `happy-transformer/examples/train_happyroberta.py`

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

* dataset_creation - all code to do with the creation of datasets
* experiment_utils - all code to with the running of experiments
* evaluation_utils - all code to with the evaluation of experiments
* plot_nbs - all notebooks, but mainly those that generate visuals of experiment results
* interpret - all code that queires allen-nlp interpretation functionality
