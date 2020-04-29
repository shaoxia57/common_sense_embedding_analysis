import torch
import random
import pandas as pd
import sys
import re

sys.path.append('../')
from dataset_creation.generate_data import pad_string
#import dataset_creation.kb_crawl.comet.src.api as comet_api

def random_string_generator_variable_size(min_size, max_size, allowed_chars):
    return ''.join(random.choice(allowed_chars) for x in range(random.randint(min_size, max_size)))

def generate_pairs_of_random_strings(number_of_pairs, min_length, max_length, character_set):
    fictitious_entities = []
    for i in range(number_of_pairs):
        word_1 = random_string_generator_variable_size(min_length, max_length, character_set)
        word_2 = random_string_generator_variable_size(min_length ,max_length ,character_set)
        fictitious_entities.append((word_1, word_2))

    return fictitious_entities

def generate_pairs_of_random_names(number_of_pairs, name_dir="../data/other/baby-names.csv"):
    names = pd.read_csv(name_dir)
    names = list(names["name"])
    name_pairs = []
    for name in random.sample(names, number_of_pairs):
        while True:
            i = random.randint(0, len(names)-1)
            if names[i] != name:
                other_name = names[i]
                name_pairs.append((name, other_name))
                break

    return name_pairs

def prepare_masked_easy_instances(sentences, config, fictitious_entities, num_entity_trials):
    masked_examples = {}
    for truism in sentences:
        for perturbation in sentences[truism]:
            candidate_answers = config[truism]['premise_switch']['0']
            for premise in sentences[truism][perturbation]:
                key = "-".join([truism, perturbation, premise])
                
                statement = sentences[truism][perturbation][premise]
                parts = statement.split(",")
                masked_portion = parts[len(parts)-1]

                right_answer = None
                wrong_answer = None
                for answer in candidate_answers:
                    if pad_string(answer, False) in masked_portion:
                        masked_portion = masked_portion.replace(" " + answer + " ", " <mask> ")
                        right_answer = answer
                    else:
                        wrong_answer = answer

                masked_statement = ""
                for i in range(len(parts)-1):
                    masked_statement += parts[i]
                    masked_statement += ","

                if right_answer and wrong_answer:
                    masked_statement += masked_portion
                    masked_examples[key] = []
                    for entity_pair in random.sample(fictitious_entities, num_entity_trials):
                        new_masked_statement = re.sub(r"\bA\b", entity_pair[0], masked_statement)
                        new_masked_statement = re.sub(r"\bB\b", entity_pair[1], new_masked_statement)
                        masked_examples[key].append((new_masked_statement, right_answer, wrong_answer))



    return masked_examples

def prepare_masked_instances(sentences, config, fictitious_entities, num_entity_trials):
    masked_examples = {}
    for truism in sentences:
        for perturbation in sentences[truism]:

            if 'paraphrase' not in perturbation:
                candidate_answers = config[truism]['premise_switch']['0']
            elif '_inversion' not in perturbation:
                candidate_answers = config[truism]['premise_switch']['1']
            else:
                candidate_answers = config[truism]['premise_switch']['2']

            for premise in sentences[truism][perturbation]:
                key = "-".join([truism, perturbation, premise])
                
                statement = sentences[truism][perturbation][premise]
                premise = statement.split(",")[0]
                conclusion = statement.split(",")[1]

                right_answer = None
                wrong_answer = None
                for answer in candidate_answers:
                    if pad_string(answer, False) in conclusion:
                        conclusion = conclusion.replace(" " + answer + " ", " <mask> ")
                        right_answer = answer
                    else:
                        wrong_answer = answer

                if right_answer and wrong_answer:
                    masked_statement = premise + "," + conclusion
                    masked_examples[key] = []
                    for entity_pair in random.sample(fictitious_entities, num_entity_trials):
                        new_masked_statement = re.sub(r"\bA\b", entity_pair[0], masked_statement)
                        new_masked_statement = re.sub(r"\bB\b", entity_pair[1], new_masked_statement)
                        masked_examples[key].append((new_masked_statement, right_answer, wrong_answer))

    return masked_examples

def prepare_masked_instances_for_humans(sentences, config):
    masked_examples = {}
    for truism in sentences:
        for perturbation in sentences[truism]:

            if 'paraphrase' not in perturbation:
                candidate_answers = config[truism]['premise_switch']['0']
            elif '_inversion' not in perturbation:
                candidate_answers = config[truism]['premise_switch']['1']
            else:
                candidate_answers = config[truism]['premise_switch']['2']

            for premise in sentences[truism][perturbation]:
                key = "-".join([truism, perturbation, premise])
                
                statement = sentences[truism][perturbation][premise]
                premise = statement.split(",")[0]
                conclusion = statement.split(",")[1]

                right_answer = None
                wrong_answer = None
                for answer in candidate_answers:
                    if pad_string(answer, False) in conclusion:
                        conclusion = conclusion.replace(" " + answer + " ", " _____ ")
                        right_answer = answer
                    else:
                        wrong_answer = answer

                if right_answer and wrong_answer:
                    masked_statement = premise + ", " + conclusion
                    masked_examples[key] = (masked_statement, right_answer, wrong_answer)

    return masked_examples

def prepare_sentence_pair(sentences, fictitious_entities, num_entity_trials):
    sentence_pairs = {}
    for index, corr_incorr_pair in sentences.items():
        sentence_pairs[index]={'correct':[],'incorrect':[]}
                
        correct_statement = corr_incorr_pair['correct']
        premise = correct_statement.split(",")[0]+'.'
        conclusion = correct_statement.split(",")[1][4:]+'.'
                
        for entity_pair in random.sample(fictitious_entities, num_entity_trials):
            filled_premise = re.sub(r"\bA\b", entity_pair[0], premise)
            filled_premise = re.sub(r"\bB\b", entity_pair[1], filled_premise).capitalize()
            filled_conclusion = re.sub(r"\bA\b", entity_pair[0], conclusion)
            filled_conclusion = re.sub(r"\bB\b", entity_pair[1], filled_conclusion).capitalize()
            sentence_pairs[index]['correct'].append((filled_premise, filled_conclusion))
            
        incorrect_statement = corr_incorr_pair['incorrect']
        premise = incorrect_statement.split(",")[0]+'.'
        conclusion = incorrect_statement.split(",")[1][4:]+'.'
                
        for entity_pair in random.sample(fictitious_entities, num_entity_trials):
            filled_premise = re.sub(r"\bA\b", entity_pair[0], premise)
            filled_premise = re.sub(r"\bB\b", entity_pair[1], filled_premise).capitalize()
            filled_conclusion = re.sub(r"\bA\b", entity_pair[0], conclusion)
            filled_conclusion = re.sub(r"\bB\b", entity_pair[1], filled_conclusion).capitalize()
            sentence_pairs[index]['incorrect'].append((filled_premise, filled_conclusion))
            
    return sentence_pairs

def tokenize_sentence(sentence, tokenizer):
    return [tokenizer.bos_token] + tokenizer.tokenize(sentence) + [tokenizer.eos_token]

def prepare_truism_data_for_sentence_scoring(sentences, possible_characters, tokenizer, num_trials):

    if len(possible_characters[0]) == 1:
        character_pairs = []
        for char in possible_characters:
            for char_2 in possible_characters:
                if char != char_2:
                    character_pairs.append((char, char_2))
    else:
        character_pairs = possible_characters

    prepped_sentences = {}
    for key in sentences:
        prepped_sentences[key] = {}
        for character_pair in random.sample(character_pairs, num_trials):
            for version in sentences[key]:
                sentence = sentences[key][version]
                sentence = re.sub(r"\bA\b", character_pair[0], sentence)
                sentence = re.sub(r"\bB\b", character_pair[1], sentence)

                tokenized_sentence = tokenize_sentence(sentence, tokenizer)
                tensor = torch.tensor(tokenizer.convert_tokens_to_ids(tokenized_sentence))
                
                if version in prepped_sentences[key]:
                    prepped_sentences[key][version].append(tensor)
                else:
                    prepped_sentences[key][version] = [tensor]
        

    return prepped_sentences

def prepare_truism_data_for_sentence_scoring_comet(sentences, possible_characters, encoder, data_loader, num_trials):

    character_pairs = []
    for char in possible_characters:
        for char_2 in possible_characters:
            if char != char_2:
                character_pairs.append((char, char_2))

    prepped_sentences = {}
    for key in sentences:
        prepped_sentences[key] = {}
        for character_pair in random.sample(character_pairs, num_trials):
            for version in sentences[key]:
                sentence = sentences[key][version]
                sentence = re.sub(r"\bA\b", character_pair[0], sentence)
                sentence = re.sub(r"\bB\b", character_pair[1], sentence)
                tokenized_sentence = comet_api.encode_sequence(sentence, encoder, data_loader)
                tensor = torch.tensor(tokenized_sentence)
                
                if version in prepped_sentences[key]:
                    prepped_sentences[key][version].append(tensor)
                else:
                    prepped_sentences[key][version] = [tensor]
        

    return prepped_sentences
