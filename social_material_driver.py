import torch
import random
import json
from random import randint
import string

random.seed(1012)
roberta = torch.hub.load(github='pytorch/fairseq', model='roberta.large')
chars = string.ascii_lowercase

def random_string_generator_variable_size(min_size, max_size, allowed_chars):
    return ''.join(random.choice(allowed_chars) for x in range(randint(min_size, max_size)))
    
with open("truism_data/material_data_sentences.json", "r") as f:
    material_data = json.load(f)
    
with open("truism_data/material_data.json", "r") as f:
    material_config = json.load(f)
    
with open("truism_data/social_data_sentences.json", "r") as f:
    social_data = json.load(f)
    
with open("truism_data/social_data.json", "r") as f:
    social_config = json.load(f)


fictitious_entities = []
for i in range(100):
    word_1 = random_string_generator_variable_size(3,12,chars)
    word_2 = random_string_generator_variable_size(3,12,chars)
    fictitious_entities.append((word_1, word_2))

material_10_results = [] # {'0':{'antonym':{'asymmetric_conclusion':{'masked_sent':'...', 'avg_score': xx}, '...'}, '...'}, 'x'}
for index, truism in material_data.items(): # Each truism: we have 5 types
#     truism['candidate_answers'] = [physical_config[index]['original_comparison'], \
#                                    physical_config[index]['antonym_comparison']] # Add candidate answers for masks
    for perturb_type, sub_truism in truism.items(): # Each perturb type (negation, antonum, etc, excluding asymmetry)
#         if 'negation_paraphrase' in perturb_type:
#             continue
        if 'paraphrase' not in perturb_type:
            candidate_answers = material_config[index]['premise_switch']['0']
        elif '_inversion' not in perturb_type:
            candidate_answers = material_config[index]['premise_switch']['1']
        else:
            candidate_answers = material_config[index]['premise_switch']['2']
        for sub_type, sent in sub_truism.items(): # Original, asymmetric premise, and asymmetric conclusion
            masked_sent = ''
            filled_sent = ''
            right_answer = ''
            wrong_answer = ''
            for answer in candidate_answers:
                if answer in sent.split(',')[1].split(): # We only mask the second half (conclusion)
                    masked_sent_half = str.replace(sent.split(',')[1], ' '+answer, ' <mask>')
                    masked_sent = sent.split(',')[0]+','+masked_sent_half
                    # print(masked_sent)
                    right_answer = answer
                else:
                    wrong_answer = answer
            if masked_sent == '':
                # print(sent)
                # print(candidate_answers)
                continue
            #if right_answer
            binary_avg_score = 0
            ratio_avg_score = 0
            for j in range(len(fictitious_entities)):
                k = random.randint(0, len(fictitious_entities)-1)
                fill_A = str.replace(masked_sent, 'A', fictitious_entities[k][0])
                filled_sent = str.replace(fill_A, 'B', fictitious_entities[k][1])
                if j == 10:
                    break
                answer_list = roberta.fill_mask(filled_sent, topk=100)
                right_pos = -1
                wrong_pos = -1
                right_score = -1
                wrong_score = -1
                for i in range(len(answer_list)):
                    if answer_list[i][2][1:] == right_answer:
                        right_score = answer_list[i][1]
                        right_pos = i
                    if answer_list[i][2][1:] == wrong_answer:
                        wrong_score = answer_list[i][1]
                        wrong_pos = i
                    if right_score != -1 and wrong_score != -1:
                        break
                if right_score == -1:
                    # print('No right answer in top 100 for '+str(filled_sent))
                    binary_score = 0
                    ratio_score = 0
                elif wrong_score == -1:
                    wrong_score = 0
                    wrong_pos = 1000
                else:
                    binary_score = 1 if right_pos < wrong_pos else 0
                    ratio_score = (right_score - wrong_score) / (right_score + wrong_score)
                binary_avg_score += binary_score
                ratio_avg_score += ratio_score
            binary_avg_score /= 10
            ratio_avg_score /= 10
            material_10_results.append(str(index)+','+str(perturb_type)+','+str(sub_type)+','+str(binary_avg_score)+','+str(ratio_avg_score))

    # print("done with {}".format(str(index)))

social_10_results = [] # {'0':{'antonym':{'asymmetric_conclusion':{'masked_sent':'...', 'avg_score': xx}, '...'}, '...'}, 'x'}
for index, truism in social_data.items(): # Each truism: we have 5 types
#     truism['candidate_answers'] = [physical_config[index]['original_comparison'], \
#                                    physical_config[index]['antonym_comparison']] # Add candidate answers for masks
    for perturb_type, sub_truism in truism.items(): # Each perturb type (negation, antonum, etc, excluding asymmetry)
#         if 'negation_paraphrase' in perturb_type:
#             continue
        if 'paraphrase' not in perturb_type:
            candidate_answers = social_config[index]['premise_switch']['0']
        elif '_inversion' not in perturb_type:
            candidate_answers = social_config[index]['premise_switch']['1']
        else:
            candidate_answers = social_config[index]['premise_switch']['2']
        for sub_type, sent in sub_truism.items(): # Original, asymmetric premise, and asymmetric conclusion
            masked_sent = ''
            filled_sent = ''
            right_answer = ''
            wrong_answer = ''
            for answer in candidate_answers:
                if answer in sent.split(',')[1].split(): # We only mask the second half (conclusion)
                    masked_sent_half = str.replace(sent.split(',')[1], ' '+answer, ' <mask>')
                    masked_sent = sent.split(',')[0]+','+masked_sent_half
                    # print(masked_sent)
                    right_answer = answer
                else:
                    wrong_answer = answer
            if masked_sent == '':
                # print(sent)
                # print(candidate_answers)
                continue
            #if right_answer
            binary_avg_score = 0
            ratio_avg_score = 0
            for j in range(len(fictitious_entities)):
                k = random.randint(0, len(fictitious_entities)-1)
                fill_A = str.replace(masked_sent, 'A', fictitious_entities[k][0])
                filled_sent = str.replace(fill_A, 'B', fictitious_entities[k][1])
                if j == 10:
                    break
                answer_list = roberta.fill_mask(filled_sent, topk=100)
                right_pos = -1
                wrong_pos = -1
                right_score = -1
                wrong_score = -1
                for i in range(len(answer_list)):
                    if answer_list[i][2][1:] == right_answer:
                        right_score = answer_list[i][1]
                        right_pos = i
                    if answer_list[i][2][1:] == wrong_answer:
                        wrong_score = answer_list[i][1]
                        wrong_pos = i
                    if right_score != -1 and wrong_score != -1:
                        break
                if right_score == -1:
                    # print('No right answer in top 100 for '+str(filled_sent))
                    binary_score = 0
                    ratio_score = 0
                elif wrong_score == -1:
                    wrong_score = 0
                    wrong_pos = 1000
                else:
                    binary_score = 1 if right_pos < wrong_pos else 0
                    ratio_score = (right_score - wrong_score) / (right_score + wrong_score)
                binary_avg_score += binary_score
                ratio_avg_score += ratio_score
            binary_avg_score /= 10
            ratio_avg_score /= 10
            social_10_results.append(str(index)+','+str(perturb_type)+','+str(sub_type)+','+str(binary_avg_score)+','+str(ratio_avg_score))

    # print("done with {}".format(str(index)))


with open('material_10_rand_entities_results','w') as f:
    for result in material_10_results:
        f.write(result)
        f.write('\n')
        
with open('social_10_rand_entities_results','w') as f:
    for result in social_10_results:
        f.write(result)
        f.write('\n')