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

    physical_sentences = proc.prep_ft_instances_for_sampling_from_sets(physical_sents, 
                                                                     physical_config, 
                                                                     fictitious_entities,
                                                                     number_of_entity_trials)

    split_sentences, split_indicies = proc.sample_from_sets_finetuning_instances(physical_sentences,
                                                                                 19,
                                                                                 2)
    phy_train_sents, phy_eval_sents, phy_test_sents = split_sentences
    phy_train_keys, phy_eval_keys, phy_test_keys = split_indicies

    with open("../data/truism_data/material_data_sentences_2.json", "r") as f:
        material_sents = json.load(f)
        
    with open("../data/truism_data/material_data_2.json", "r") as f:
        material_config = json.load(f)

    logger.info("finished reading in material data")

    material_sentences = proc.prep_ft_instances_for_sampling_from_sets(material_sents, 
                                                                     material_config, 
                                                                     fictitious_entities,
                                                                     number_of_entity_trials)

    split_sentences, split_indicies = proc.sample_from_sets_finetuning_instances(material_sentences,
                                                                                 19,
                                                                                 2)
    mat_train_sents, mat_eval_sents, mat_test_sents = split_sentences
    mat_train_keys, mat_eval_keys, mat_test_keys = split_indicies

    with open("../data/truism_data/social_data_sentences_2.json", "r") as f:
        social_sents = json.load(f)
        
    with open("../data/truism_data/social_data_2.json", "r") as f:
        social_config = json.load(f)

    logger.info("finished reading in social data")

    social_sentences = proc.prep_ft_instances_for_sampling_from_sets(social_sents, 
                                                                   social_config, 
                                                                   fictitious_entities,
                                                                   number_of_entity_trials)
    
    split_sentences, split_indicies = proc.sample_from_sets_finetuning_instances(social_sentences,
                                                                                 19,
                                                                                 2)
    soc_train_sents, soc_eval_sents, soc_test_sents = split_sentences
    soc_train_keys, soc_eval_keys, soc_test_keys = split_indicies


    train_sents = np.concatenate((phy_train_sents, mat_train_sents, soc_train_sents))
    eval_sents = np.concatenate((phy_eval_sents, mat_eval_sents, soc_eval_sents))
    test_sents = np.concatenate((phy_test_sents, mat_test_sents, soc_test_sents))

    train_keys = {
        "phy" : phy_train_keys,
        "mat" : mat_train_keys,
        "soc" : soc_train_keys
    }

    eval_keys = {
        "phy" : phy_eval_keys,
        "mat" : mat_eval_keys,
        "soc" : soc_eval_keys
    }

    test_keys = {
        "phy" : phy_test_keys,
        "mat" : mat_test_keys,
        "soc" : soc_test_keys
    }


    with open("../data/finetune_data/sample_from_sets/train_sentences.txt", "w") as f:
        for i, sent in enumerate(train_sents):
            f.write(sent[0])
            if i < len(train_sents) - 1:
                f.write("\n")

    with open("../data/finetune_data/sample_from_sets/train_m_sentences.txt", "w") as f:
        for i, sent in enumerate(train_sents):
            f.write(sent[1])
            if i < len(train_sents) - 1:
                f.write("\n")

    with open("../data/finetune_data/sample_from_sets/train_keys.json", "w") as f:
        json.dump(train_keys, f, indent=1)

    with open("../data/finetune_data/sample_from_sets/eval_sentences.txt", "w") as f:
        for i, sent in enumerate(eval_sents):
            f.write(sent[0])
            if i < len(eval_sents) - 1:
                f.write("\n")

    with open("../data/finetune_data/sample_from_sets/eval_m_sentences.txt", "w") as f:
        for i, sent in enumerate(eval_sents):
            f.write(sent[1])
            if i < len(eval_sents) - 1:
                f.write("\n")

    with open("../data/finetune_data/sample_from_sets/eval_keys.json", "w") as f:
        json.dump(eval_keys, f, indent=1)

    with open("../data/finetune_data/sample_from_sets/test_sentences.txt", "w") as f:
        for i, sent in enumerate(test_sents):
            f.write(sent[0])
            if i < len(test_sents) - 1:
                f.write("\n")

    with open("../data/finetune_data/sample_from_sets/test_m_sentences.txt", "w") as f:
        for i, sent in enumerate(test_sents):
            f.write(sent[1])
            if i < len(test_sents) - 1:
                f.write("\n")

    with open("../data/finetune_data/sample_from_sets/test_keys.json", "w") as f:
        json.dump(test_keys, f, indent=1)

if __name__ == "__main__":
    main()



