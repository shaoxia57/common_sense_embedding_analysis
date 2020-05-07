import requests
import json
import sys
import random
import string
import time
import logging
from transformers import BertTokenizer
import re

sys.path.append('../')

from dataset_creation import pre_processing_utils as proc

URL = "https://demo.allennlp.org/interpret/masked-lm"
INTERPRETER = "smooth_gradient"
tokenizer = BertTokenizer.from_pretrained('bert-base-cased')

def parse(sentence):
    # temp = sentence.split(" ")
    # full_parse = []
    # for seq in temp:
    #     if "," in seq:
    #         full_parse.append(seq[:len(seq)-1])
    #         full_parse.append(",")
    #     elif "." in seq:
    #         full_parse.append(seq[:len(seq)-1])
    #         full_parse.append(".")
    #     else:
    #         full_parse.append(seq)

    # return full_parse
    return tokenizer.tokenize(sentence)

def get_scores_from_allen_nlp(masked_sentence):

    message = {
            "sentence" : masked_sentence,
            "interpreter" : INTERPRETER
          }

    response = requests.post(URL, json = message)

    response_data = json.loads(response.text)

    gradient_scores = response_data["instance_1"]["grad_input_1"]
    # print(gradient_scores)
    # We don't need SEP or CLS token
    scores = gradient_scores[1:len(gradient_scores)-1]
    parsed_sentence = parse(masked_sentence)

    assert len(scores) == len(parsed_sentence)

    output = []

    for i, score in enumerate(scores):
        output.append((parsed_sentence[i], score))

    return output


def check_response(arr):
    for entry in arr:
        if "#" in entry[0]:
            return True
    return False

def get_scores(fictitious_entities, sentences, config, number_of_entity_trials, logger):
    dataset = proc.prepare_masked_instances(sentences=sentences, 
                                            config=config, 
                                            fictitious_entities=fictitious_entities,
                                            num_entity_trials=number_of_entity_trials)
    with open("good_responses.json") as f:
        good_responses = json.load(f)

    original_data = []
    with open("blah.txt") as f:
        for line in f:
            tup = eval(line)
            original_data.append(tup)  

    logger.info("finished creating dataset")

    output = {}
    missed = {}
    prev_output_length = 0
    stop = False
    random_count = random.randint(75, 250)
    logger.info("Initial Random Count {}".format(random_count))
    for i, key in enumerate(dataset.keys()):
        trials = dataset[key]
        output[key] = []
        missed[key] = []
        for j, entry in enumerate(trials):
            if check_response(good_responses[key][j]):
                tup = original_data[(i*5)+j]
                sent = re.sub(r"\bA\b", tup[1][0], tup[0])
                sent = re.sub(r"\bB\b", tup[1][1], sent)
                new_masked_sent = sent.replace("<mask>", "[MASK]")
            
                try:
                    scores = get_scores_from_allen_nlp(new_masked_sent)
                    output[key].append(scores)
                except AssertionError:
                    logger.info("something is up 1")
                    missed[key].append(j)
                except:
                    logger.info("something is up 2")
                    missed[key].append(j)

                random_count += -1
            
                if random_count == 0:
                    logger.info("Number Completed: {}".format(len(output)))
                    logger.info("sleeping")
                    time.sleep(random.randint(3, 12))
                    logger.info("done_sleeping {}-{}".format(i,j))
                    random_count = random.randint(75, 250)
                    logger.info("New Random Count {}".format(random_count))
            else:
                output[key].append(good_responses[key][j])

    return output, missed


def main():
    random.seed(1012)
    logging.basicConfig(format = '%(asctime)s - %(levelname)s - %(name)s -   %(message)s',
                        datefmt = '%m/%d/%Y %H:%M:%S',
                        level = logging.INFO)
    logger = logging.getLogger(__name__)
    chars = string.ascii_lowercase
    number_of_entity_trials = 5
    chars = string.ascii_lowercase
    names = proc.generate_pairs_of_random_names(number_of_pairs=100, name_dir="../data/other/filtered_names.csv")
    # print(names)
    with open("../data/truism_data/social_data_sentences_2.json", "r") as f:
        social_sents = json.load(f)
        
    with open("../data/truism_data/social_data_2.json", "r") as f:
        social_config = json.load(f)

    logger.info("finished reading in social data")

    output, missed = get_scores(names, social_sents, social_config, number_of_entity_trials, logger)

    logger.info("finished getting scores for social data")

    with open("good_responses_2.json", "w") as f:
        json.dump(output, f, indent=1)

    with open("bad_responses.json", "w") as f:
        json.dump(missed, f, indent=1)

if __name__ == "__main__":
    main()
