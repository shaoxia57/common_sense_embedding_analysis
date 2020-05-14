import json
import logging
import random
import string
import sys
import numpy as np
import pre_processing_utils as proc

def main():
    random.seed(1012)
    logging.basicConfig(format = '%(asctime)s - %(levelname)s - %(name)s -   %(message)s',
                        datefmt = '%m/%d/%Y %H:%M:%S',
                        level = logging.INFO)
    logger = logging.getLogger(__name__)
    chars = string.ascii_lowercase
    number_of_entity_trials = 10
    fictitious_entities = proc.generate_pairs_of_random_strings(number_of_pairs=100, 
                                                                min_length=3,
                                                                max_length=12,
                                                                character_set=chars)

    with open("../data/truism_data/physical_data_sentences_2.json", "r") as f:
        physical_sents = json.load(f)
        
    with open("../data/truism_data/physical_data_2.json", "r") as f:
        physical_config = json.load(f)

    logger.info("finished reading in physical data")

    physical_sentences = proc.prepare_finetuning_instances(physical_sents, 
                                                       physical_config, 
                                                       fictitious_entities,
                                                       number_of_entity_trials)

    with open("../data/truism_data/material_data_sentences_2.json", "r") as f:
        material_sents = json.load(f)
        
    with open("../data/truism_data/material_data_2.json", "r") as f:
        material_config = json.load(f)

    logger.info("finished reading in material data")

    material_sentences = proc.prepare_finetuning_instances(material_sents, 
                                                           material_config, 
                                                           fictitious_entities,
                                                           number_of_entity_trials)

    with open("../data/truism_data/social_data_sentences_2.json", "r") as f:
        social_sents = json.load(f)
        
    with open("../data/truism_data/social_data_2.json", "r") as f:
        social_config = json.load(f)

    logger.info("finished reading in social data")

    social_sentences = proc.prepare_finetuning_instances(social_sents, 
                                                         social_config, 
                                                         fictitious_entities,
                                                         number_of_entity_trials)

    sentences = np.concatenate((physical_sentences, material_sentences, social_sentences))


    split_sentences, split_indicies = proc.sample_finetuning_instances(sentences,
                                                                       train_pct=0.8,
                                                                       eval_pct=0.1)
    
    train_sents, eval_sents, test_sents = split_sentences
    train_sets, eval_sets, test_sets = split_indicies


    with open("../data/finetune_data/train_sentences.txt", "w") as f:
        for i, sent in enumerate(train_sents):
            f.write(sent[0])
            if i < len(train_sents) - 1:
                f.write("\n")

    with open("../data/finetune_data/train_m_sentences.txt", "w") as f:
        for i, sent in enumerate(train_sents):
            f.write(sent[1])
            if i < len(train_sents) - 1:
                f.write("\n")

    with open("../data/finetune_data/train_sets.txt", "w") as f:
        f.write(str(train_sets))

    with open("../data/finetune_data/eval_sentences.txt", "w") as f:
        for i, sent in enumerate(eval_sents):
            f.write(sent[0])
            if i < len(eval_sents) - 1:
                f.write("\n")

    with open("../data/finetune_data/eval_m_sentences.txt", "w") as f:
        for i, sent in enumerate(eval_sents):
            f.write(sent[1])
            if i < len(eval_sents) - 1:
                f.write("\n")

    with open("../data/finetune_data/eval_sets.txt", "w") as f:
        f.write(str(eval_sets))

    with open("../data/finetune_data/test_sentences.txt", "w") as f:
        for i, sent in enumerate(test_sents):
            f.write(sent[0])
            if i < len(test_sents) - 1:
                f.write("\n")

    with open("../data/finetune_data/test_m_sentences.txt", "w") as f:
        for i, sent in enumerate(test_sents):
            f.write(sent[1])
            if i < len(test_sents) - 1:
                f.write("\n")

    with open("../data/finetune_data/test_sets.txt", "w") as f:
        f.write(str(test_sets))

if __name__ == "__main__":
    main()



