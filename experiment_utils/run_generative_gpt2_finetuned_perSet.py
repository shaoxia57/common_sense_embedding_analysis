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

    tokenizer = GPT2Tokenizer.from_pretrained('../../models/gpt-2/sample_from_set')
    model = GPT2LMHeadModel.from_pretrained("../../models/gpt-2/sample_from_set")

    with open("../data/generation_test_data/physical_data_sentences.json", "r") as f:
        physical_sents = json.load(f)

    with open("../data/finetune_data/sample_from_sets/test_keys.json", "r") as f:
        test_keys = json.load(f)

    phy_filtered = {}
    for key in test_keys['phy']:
        phy_filtered[key] = physical_sents[key]

    logger.info("finished reading in physical data")

    output_df = run_pipeline(model=model,
                             tokenizer=tokenizer,
                             possible_chars=chars, 
                             sentences=phy_filtered, 
                             number_of_trials=number_of_trials,
                             logger=logger)

    output_df.to_csv("../data/generation_result_data/gpt2/sample_from_set/physical_perf_ft_{}.csv".format(number_of_trials),
                     index=False)

    logger.info("finished saving physical dataset results")

        
    with open("../data/generation_test_data/material_data_sentences.json", "r") as f:
        material_sents = json.load(f)
        
    with open("../data/finetune_data/sample_from_sets/test_keys.json", "r") as f:
        test_keys = json.load(f)

    mat_filtered = {}
    for key in test_keys['mat']:
        mat_filtered[key] = material_sents[key]

    logger.info("finished reading in physical data")

    logger.info("finished reading in material data")

    output_df = run_pipeline(model=model,
                             tokenizer=tokenizer,
                             possible_chars=chars, 
                             sentences=mat_filtered, 
                             number_of_trials=number_of_trials,
                             logger=logger)

    output_df.to_csv("../data/generation_result_data/gpt2/sample_from_set/material_perf_ft_{}.csv".format(number_of_trials),
                     index=False)

    logger.info("finished saving material dataset results")
        
    with open("../data/generation_test_data/social_data_sentences.json", "r") as f:
        social_sents = json.load(f)

    with open("../data/finetune_data/sample_from_sets/test_keys.json", "r") as f:
        test_keys = json.load(f)

    soc_filtered = {}
    for key in test_keys['soc']:
        soc_filtered[key] = social_sents[key]

    logger.info("finished reading in physical data")

    logger.info("finished reading in social data")

    output_df = run_pipeline(model=model,
                             tokenizer=tokenizer,
                             possible_chars=chars, 
                             sentences=soc_filtered, 
                             number_of_trials=number_of_trials,
                             logger=logger)

    output_df.to_csv("../data/generation_result_data/gpt2/sample_from_set/social_perf_ft_{}.csv".format(number_of_trials),
                     index=False)

    logger.info("finished saving social dataset results")

if __name__ == "__main__":
    main()
