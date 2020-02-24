import torch
import random
import pandas as pd
from fairseq.data.data_utils import collate_tokens

def random_string_generator_variable_size(min_size, max_size, allowed_chars):
    return ''.join(random.choice(allowed_chars) for x in range(random.randint(min_size, max_size)))

def generate_pairs_of_random_strings(number_of_pairs, min_length, max_length, character_set):
    fictitious_entities = []
    for i in range(number_of_pairs):
        word_1 = random_string_generator_variable_size(min_length, max_length, character_set)
        word_2 = random_string_generator_variable_size(min_length ,max_length ,character_set)
        fictitious_entities.append((word_1, word_2))

    return fictitious_entities

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

                right_answer = candidate_answers[0]
                wrong_answer = candidate_answers[1]

                masked_portion = masked_portion.replace(" " + right_answer + " ", " <mask> ")
                
                masked_statement = ""
                for i in range(len(parts)-1):
                    masked_statement += parts[i]
                    masked_statement += ","

                masked_statement += masked_portion
                masked_examples[key] = []
                for entity_pair in random.sample(fictitious_entities, num_entity_trials):
                    new_masked_statement = masked_statement.replace("A", entity_pair[0])
                    new_masked_statement = new_masked_statement.replace("B", entity_pair[1])
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
                    if answer in conclusion:
                        conclusion = conclusion.replace(" " + answer + " ", " <mask> ")
                        right_answer = answer
                    else:
                        wrong_answer = answer

                if right_answer and wrong_answer:
                    masked_statement = premise + ", " + conclusion
                    masked_examples[key] = []
                    for entity_pair in random.sample(fictitious_entities, num_entity_trials):
                        new_masked_statement = masked_statement.replace("A", entity_pair[0])
                        new_masked_statement = new_masked_statement.replace("B", entity_pair[1])
                        masked_examples[key].append((new_masked_statement, right_answer, wrong_answer))

    return masked_examples

def prepare_sentence_pair(sentences, config, fictitious_entities, num_entity_trials):
    sentence_pairs = {}
    for truism in sentences:
        for perturbation in sentences[truism]:
            for asym_perturb in sentences[truism][perturbation]:
                key = "-".join([truism, perturbation, asym_perturb])
                
                statement = sentences[truism][perturbation][asym_perturb]
                premise = statement.split(",")[0]+'.'
                conclusion = statement.split(",")[1][4:]+'.'
                
                sentence_pairs[key] = []
                for entity_pair in random.sample(fictitious_entities, num_entity_trials):
                    filled_premise = premise.replace("A", entity_pair[0]).replace("B", entity_pair[1]).capitalize()
                    filled_conclusion = conclusion.replace("A", entity_pair[0]).replace("B", entity_pair[1]).capitalize()
                    sentence_pairs[key].append((filled_premise, filled_conclusion))

    return sentence_pairs

def tokenize_sentence(sentence, tokenizer):
    return [tokenizer.bos_token] + tokenizer.tokenize(sentence) + [tokenizer.eos_token]

def prepare_truism_data_for_sentence_scoring(sentences, possible_characters, tokenizer, num_trials):

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
                sentence = sentence.replace("A", character_pair[0]).replace("B", character_pair[1])

                tokenized_sentence = tokenize_sentence(sentence, tokenizer)
                tensor = torch.tensor(tokenizer.convert_tokens_to_ids(tokenize_sentence))
                
                if version in prepped_sentences[key]:
                    prepped_sentences[key][version].append(tensor)
                else:
                    prepped_sentences[key][version] = [tensor]
        

    return prepped_sentences

def generative_truism_reasoning_test(tensors, model, gpu_available, logger):
    if gpu_available:
        for key in tensors:
            for version in tensors[key]:
                for i, tensor in enumerate(tensors[key][version]):
                tensors[key][version][i] = tensor.cuda()
        logger.info("successfully moved tensors to gpu")

        model.cuda()
        logger.info("successfully moved model to gpu")

    model.eval()

    avg_responses = {}
    with torch.no_grad():
        for j, key in enumerate(tensors):
            binary_avg_score = 0.0
            ratio_avg_score = 0.0
            num_trials = len(tensors[key]["correct"])
            for i in range(num_trials):
                right_tensor = tensors[key]["correct"][i]
                wrong_tensor = tensors[key]["incorrect"][i]
                right_answer_outputs = model(right_tensor, labels=right_tensor)
                wrong_answer_outputs = model(wrong_tensor, labels=wrong_tensor)

                right_answer_perp = math.exp(right_answer_outputs[0].item())
                wrong_answer_perp = math.exp(wrong_answer_outputs[0].item())
            
                if right_answer_perp < wrong_answer_perp:
                    binary_avg_score += 1

                ratio_avg_score += (wrong_answer_perp - right_answer_perp) / (wrong_answer_perp + right_answer_perp)

            binary_avg_score = binary_avg_score / float(num_trials)
            ratio_avg_score = ratio_avg_score / float(num_trials)

            avg_responses[key] = {"binary_score" : binary_avg_score, "ratio_score" : ratio_avg_score}
        
        if (j+1) % 240 == 0:
            logger.info("finished 10 more")

    return avg_responses

def fair_seq_masked_word_prediction(masked_examples, model, gpu_available, top_n, logger):
    if gpu_available:
        model.cuda()
        logger.info("successfully moved model to gpu")

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

def fair_seq_sent_pair_classification(sentence_pairs, model, gpu_available, logger):
    if gpu_available:
        model.cuda()
        logger.info("successfully moved model to gpu")

    model.eval()

    avg_responses = {}
    counter = 0
    for key, pairs in sentence_pairs.items():
        
        batch = collate_tokens([model.encode(pair[0], pair[1]) for pair in pairs], pad_idx=1)
        logprobs = model.predict('mnli', batch)
        
        result_list = logprobs.argmax(dim=1).tolist()
        avg_accuracy = result_list.count(2)/len(result_list)

        avg_responses[key] = avg_accuracy
        counter += 1
        if counter % 24 == 0:
            logger.info("finished one set")

    return avg_responses

def convert_bi_statistic_results_into_df(result_dictionary):
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


def convert_fair_seq_sent_pair_results_into_df(result_dictionary):
    set_numbers = []
    perturbations = []
    asym_perturbs = []
    avg_accuracy_scores = []
    for key in result_dictionary:
        parts = key.split("-")
        set_numbers.append(int(parts[0]))
        perturbations.append(parts[1])
        asym_perturbs.append(parts[2])
        avg_accuracy_scores.append(result_dictionary[key])

    return pd.DataFrame.from_dict({
            "set_number"    : set_numbers,
            "perturbation"     : perturbations,
            "asym_perturbs"          : asym_perturbs,
            "avg_accuracy_score" : avg_accuracy_scores,
        })