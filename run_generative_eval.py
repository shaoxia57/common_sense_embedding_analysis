import torch
from transformers import GPT2Tokenizer, GPT2LMHeadModel
import random
import json
import string
import logging
from experiment_utils import *

def run_pipeline(model, tokenizer, possible_chars, sentences, number_of_trials, logger):
    
    dataset = prepare_truism_data_for_sentence_scoring(sentences,
                                                       possible_chars,
                                                       tokenizer,
                                                       number_of_trials)

    logger.info("finished creating dataset")

    perf = generative_truism_reasoning_test(dataset, model, torch.cuda.is_available(), logger)

    logger.info("finished evaluating dataset")
    
    output_df = convert_bi_statistic_results_into_df(perf)

    return output_df

def main():
    random.seed(1012)
    logging.basicConfig(format = '%(asctime)s - %(levelname)s - %(name)s -   %(message)s',
                        datefmt = '%m/%d/%Y %H:%M:%S',
                        level = logging.INFO)
    logger = logging.getLogger(__name__)
    chars = list(string.ascii_uppercase.replace("A", "").replace("I", "").replace("U", ""))
    number_of_trials = 10

    tokenizer = GPT2Tokenizer.from_pretrained('gpt2')
    model = GPT2LMHeadModel.from_pretrained("gpt2")

    with open("generative_lm_test_data/physical_data_sentences.json", "r") as f:
        physical_sents = json.load(f)

    logger.info("finished reading in physical data")

    output_df = run_pipeline(model=model,
                             tokenizer=tokenizer,
                             possible_chars=chars, 
                             sentences=physical_sents, 
                             number_of_trials=number_of_trials,
                             logger=logger)

    output_df.to_csv("generative_result_data/physical_perf_{}.csv".format(number_of_trials),
                     index=False)

    logger.info("finished saving physical dataset results")

        
    with open("generative_lm_test_data/material_data_sentences.json", "r") as f:
        material_sents = json.load(f)
        

    logger.info("finished reading in material data")

    output_df = run_pipeline(model=model,
                             tokenizer=tokenizer,
                             possible_chars=chars, 
                             sentences=material_sents, 
                             number_of_trials=number_of_trials,
                             logger=logger)

    output_df.to_csv("generative_result_data/material_perf_{}.csv".format(number_of_trials),
                     index=False)

    logger.info("finished saving material dataset results")
        
    with open("generative_lm_test_data/social_data_sentences.json", "r") as f:
        social_sents = json.load(f)

    logger.info("finished reading in social data")

    output_df = run_pipeline(model=model,
                             tokenizer=tokenizer,
                             possible_chars=chars, 
                             sentences=social_sents, 
                             number_of_trials=number_of_trials,
                             logger=logger)

    output_df.to_csv("generative_result_data/social_perf_{}.csv".format(number_of_trials),
                     index=False)

    logger.info("finished saving social dataset results")

if __name__ == "__main__":
    main()
