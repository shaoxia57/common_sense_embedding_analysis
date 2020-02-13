import torch
import random
import pandas as pd

def random_string_generator_variable_size(min_size, max_size, allowed_chars):
    return ''.join(random.choice(allowed_chars) for x in range(random.randint(min_size, max_size)))

def generate_pairs_of_random_strings(number_of_pairs, min_length, max_length, character_set):
    fictitious_entities = []
    for i in range(number_of_pairs):
        word_1 = random_string_generator_variable_size(min_length, max_length, character_set)
        word_2 = random_string_generator_variable_size(min_length ,max_length ,character_set)
        fictitious_entities.append((word_1, word_2))

    return fictitious_entities

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
                    if answer in conclusion:
                        conclusion = conclusion.replace(" " + answer + " ", " <mask> ")
                        right_answer = answer
                    else:
                        wrong_answer = answer

                if right_answer and wrong_answer:
                    masked_statement = premise + ", " + conclusion
                    masked_examples[key] = []
                    for entity_pair in random.sample(fictitious_entities, num_entity_trials):
                        masked_statement = masked_statement.replace("A", entity_pair[0])
                        masked_statement = masked_statement.replace("B", entity_pair[1])
                        masked_examples[key].append((masked_statement, right_answer, wrong_answer))

    return masked_examples

def fair_seq_masked_word_prediction(masked_examples, model, gpu_available, top_n, logger):
    if gpu_available:
        model.cuda()
        logger.info("succefully moved model to gpu")

    model.eval()

    avg_responses = {}
    for j, key in enumerate(masked_examples):
        binary_avg_score = 0
        ratio_avg_score = 0

        for example in masked_examples[key]:
            statement, right_answer, wrong_answer = example
            responses = model.fill_mask(statement, topk=top_n)
            right_pos = top_n + 1
            wrong_pos = top_n + 1
            right_score = 0
            wrong_score = 0
            done = -1
            for i in range(len(responses)):
                possible_answer = responses[i][2].strip().lower()
                if possible_answer == right_answer:
                    right_score = responses[i][1]
                    right_pos = i
                    done += 1
                if possible_answer == wrong_answer:
                    wrong_score = responses[i][1]
                    wrong_pos = i
                    done += 1
                if done > 0:
                    break
            
            binary_score = 1 if right_pos < wrong_pos else 0
            
            if right_score + wrong_score > 0:
                ratio_score = (right_score - wrong_score) / (right_score + wrong_score)
            else:
                ratio_score = -1
            
            binary_avg_score += binary_score
            ratio_avg_score += ratio_score

        binary_avg_score /= float(len(masked_examples[key]))
        ratio_avg_score /= float(len(masked_examples[key]))

        avg_responses[key] = {"binary_score" : binary_avg_score, "ratio_score" : ratio_avg_score}
        
        if (j+1) % 240 == 0:
            logger.info("finished 10 more")

    return avg_responses

def convert_fair_seq_results_into_df(result_dictionary):
    truism_numbers = []
    perturbations = []
    premises = []
    avg_binary_scores = []
    avg_ratio_scores = []
    for key in result_dictionary:
        parts = key.split("-")
        truism_numbers.append(int(parts[0]))
        perturbations.append(parts[1])
        premises.append(parts[2])
        avg_binary_scores.append(result_dictionary[key]["binary_score"])
        avg_ratio_scores.append(result_dictionary[key]["ratio_score"])

    return pd.DataFrame.from_dict({
            "truism_number"    : truism_numbers,
            "perturbation"     : perturbations,
            "premise"          : premises,
            "avg_binary_score" : avg_binary_scores,
            "avg_ratio_score"  : avg_ratio_scores
        })