import json
import sys
import logging
import random
import string
import torch
from transformers import GPT2Tokenizer, GPT2LMHeadModel, OpenAIGPTTokenizer, OpenAIGPTLMHeadModel
import experiment_utils as utils

sys.path.append('../')
from dataset_creation import pre_processing_utils as proc

def run_pipeline(model, tokenizer, possible_chars, sentences, number_of_trials, logger):
    
    dataset = proc.prepare_truism_data_for_sentence_scoring(sentences,
                                                       possible_chars,
                                                       tokenizer,
                                                       number_of_trials)

    logger.info("finished creating dataset")

    perf = utils.generative_truism_reasoning_test(dataset, model, torch.cuda.is_available(), logger)

    logger.info("finished evaluating dataset")
    
    output_df = utils.convert_bi_statistic_results_into_df(perf)

    return output_df

def main():
    random.seed(1012)
    logging.basicConfig(format = '%(asctime)s - %(levelname)s - %(name)s -   %(message)s',
                        datefmt = '%m/%d/%Y %H:%M:%S',
                        level = logging.INFO)
    logger = logging.getLogger(__name__)
    chars = list(string.ascii_uppercase.replace("A", "").replace("I", "").replace("U", ""))
    number_of_trials = 10

    tokenizer = GPT2Tokenizer.from_pretrained('../../models/gpt-2/')
    model = GPT2LMHeadModel.from_pretrained("../../models/gpt-2/")

    with open("../data/generation_test_data/physical_data_sentences.json", "r") as f:
        physical_sents = json.load(f)

    test_index = ['15','18']
    test_phy_sents = {}
    for key, val in physical_sents.items():
        if key.split('-')[0] in test_index:
            test_phy_sents[key] = val

    logger.info("finished reading in physical data")

    output_df = run_pipeline(model=model,
                             tokenizer=tokenizer,
                             possible_chars=chars, 
                             sentences=test_phy_sents, 
                             number_of_trials=number_of_trials,
                             logger=logger)

    output_df.to_csv("../data/generation_result_data/gpt2/physical_perf_ft_{}.csv".format(number_of_trials),
                     index=False)

    logger.info("finished saving physical dataset results")

        
    with open("../data/generation_test_data/material_data_sentences.json", "r") as f:
        material_sents = json.load(f)
        
    test_index = ['15','18']
    test_mat_sents = {}
    for key, val in material_sents.items():
        if key.split('-')[0] in test_index:
            test_mat_sents[key] = val

    logger.info("finished reading in material data")

    output_df = run_pipeline(model=model,
                             tokenizer=tokenizer,
                             possible_chars=chars, 
                             sentences=test_mat_sents, 
                             number_of_trials=number_of_trials,
                             logger=logger)

    output_df.to_csv("../data/generation_result_data/gpt2/material_perf_ft_{}.csv".format(number_of_trials),
                     index=False)

    logger.info("finished saving material dataset results")
        
    with open("../data/generation_test_data/social_data_sentences.json", "r") as f:
        social_sents = json.load(f)

    test_index = ['15','18']
    test_soc_sents = {}
    for key, val in social_sents.items():
        if key.split('-')[0] in test_index:
            test_soc_sents[key] = val

    logger.info("finished reading in social data")

    output_df = run_pipeline(model=model,
                             tokenizer=tokenizer,
                             possible_chars=chars, 
                             sentences=test_soc_sents, 
                             number_of_trials=number_of_trials,
                             logger=logger)

    output_df.to_csv("../data/generation_result_data/gpt2/social_perf_ft_{}.csv".format(number_of_trials),
                     index=False)

    logger.info("finished saving social dataset results")

if __name__ == "__main__":
    main()
