
def original_phys_perturbation(comparison, comparison_phrase, premise_switch, mode):
    negation_comparison_phrase = comparison_phrase.replace(premise_switch[mode][0], 
                                                                    premise_switch[mode][1])
    
    original = "A is " + comparison + " than B, so A " + comparison_phrase + " B"
    asymmetric_premise = "B is " + comparison + " than A, so A " + negation_comparison_phrase + " B"
    asymmetric_conclusion = "A is " + comparison + " than B, so B " + negation_comparison_phrase + " A"

    return {"original" : original, "asymmetric_premise" : asymmetric_premise, "asymmetric_conclusion" : asymmetric_conclusion}

def negative_phys_perturbation(comparison, comparison_phrase, premise_switch, mode):
    negation_comparison_phrase = comparison_phrase.replace(premise_switch[mode][0], 
                                                                    premise_switch[mode][1])

    original = "A is " +  comparison + " than B, so A " + negation_comparison_phrase + " B"
    asymmetric_premise = "B is " + comparison + " than A, so A " + comparison_phrase + " B"
    asymmetric_conclusion = "A is " + comparison + " than B, so B " + comparison_phrase + " A"

    return {"original" : original, "asymmetric_premise" : asymmetric_premise, "asymmetric_conclusion" : asymmetric_conclusion}


def generate_physical_perturbations(negation, 
                                    original_comparison,
                                    antonym_comparison,
                                    original_comparison_phrase,
                                    paraphrase,
                                    inverted_paraphrase,
                                    premise_switch):

    output = {}
    negative_comparison = negation + " " + original_comparison
    negation_antonym_comparison = negation + " " + antonym_comparison

    output["original"] = original_phys_perturbation(original_comparison, original_comparison_phrase, premise_switch, "0")
    output["negation"] = negative_phys_perturbation(negative_comparison, original_comparison_phrase, premise_switch, "0")
    output["antonym"]  = negative_phys_perturbation(antonym_comparison, original_comparison_phrase, premise_switch, "0")
    output["paraphrase"] = original_phys_perturbation(original_comparison, paraphrase, premise_switch, "1")
    output["paraphrase_inversion"] = negative_phys_perturbation(original_comparison, inverted_paraphrase, premise_switch, "2")

    output["negation_antonym"] = original_phys_perturbation(negation_antonym_comparison, original_comparison_phrase, premise_switch, "0")
    output["negation_paraphrase"] = original_phys_perturbation(negative_comparison, inverted_paraphrase, premise_switch, "2")
    output["negation_paraphrase_inversion"] = negative_phys_perturbation(negative_comparison, paraphrase, premise_switch, "1")

    output["antonym_paraphrase"] = original_phys_perturbation(antonym_comparison, inverted_paraphrase, premise_switch, "2")
    output["antonym_paraphrase_inversion"] = negative_phys_perturbation(antonym_comparison, paraphrase, premise_switch, "1")

    output["negation_antonym_paraphrase"] = original_phys_perturbation(negation_antonym_comparison, inverted_paraphrase, premise_switch, "2")
    output["negation_antonym_paraphrase_inversion"] = negative_phys_perturbation(negation_antonym_comparison, paraphrase, premise_switch, "1")

    return output


def original_material_perturbation(material_1, material_2, comparison_phrase, negation_switch, mode):
    negation_comparison_phrase = comparison_phrase.replace(negation_switch[mode][0], 
                                                           negation_switch[mode][1])
    
    original = "A is made out of " + material_1 + " and B is made out of " + material_2 + ", so A " + comparison_phrase + " B"
    asymmetric_premise = "B is made out of " + material_1 + " and A is made out of " + material_2 + ", so A " + negation_comparison_phrase + " B"
    asymmetric_conclusion = "A is made out of " + material_1 + " and B is made out of " + material_2 + ", so B " + negation_comparison_phrase + " A"

    return {"original" : original, "asymmetric_premise" : asymmetric_premise, "asymmetric_conclusion" : asymmetric_conclusion}

def negative_material_perturbation(material_1, material_2, comparison_phrase, negation_switch, mode):
    negation_comparison_phrase = comparison_phrase.replace(negation_switch[mode][0], 
                                                                    negation_switch[mode][1])

    original = "A is made out of " + material_1 + " and B is made out of " + material_2 + ", so A " + negation_comparison_phrase + " B"
    asymmetric_premise = "B is made out of " + material_1 + " and A is made out of " + material_2 + ", so A " + comparison_phrase + " B"
    asymmetric_conclusion = "A is made out of " + material_1 + " and B is made out of " + material_2 + ", so B " + comparison_phrase + " A"

    return {"original" : original, "asymmetric_premise" : asymmetric_premise, "asymmetric_conclusion" : asymmetric_conclusion}

def generate_material_perturbations(material_1,
                                    material_2,
                                    negation_switch,
                                    antonym_switch,
                                    original_comparison,
                                    paraphrase,
                                    inverted_paraphrase,
                                    premise_switch):

    output = {}
    negative_comparison = original_comparison.replace(negation_switch["0"][0], negation_switch["0"][1])
    antonym_comparison = original_comparison.replace(antonym_switch[0], antonym_switch[1])
    negation_antonym_comparison = antonym_comparison.replace(negation_switch["0"][0], negation_switch["0"][1])

    negative_paraphrase_comparison = paraphrase.replace(negation_switch["1"][0], negation_switch["1"][1])
    negative_paraphrase_inversion_comparison = inverted_paraphrase.replace(negation_switch["2"][0], negation_switch["2"][1])

    output["original"] = original_material_perturbation(material_1, material_2, original_comparison, premise_switch, "0")
    output["negation"] = negative_material_perturbation(material_1, material_2, negative_comparison, premise_switch, "0")
    output["antonym"]  = negative_material_perturbation(material_1, material_2, antonym_comparison, premise_switch, "0")
    output["paraphrase"] = original_material_perturbation(material_1, material_2, paraphrase, premise_switch, "1")
    output["paraphrase_inversion"] = negative_material_perturbation(material_1, material_2, inverted_paraphrase, premise_switch, "2")

    output["negation_antonym"] = original_material_perturbation(material_1, material_2, negation_antonym_comparison, premise_switch, "0")
    output["negation_paraphrase"] = original_material_perturbation(material_1, material_2, negative_paraphrase_inversion_comparison, premise_switch, "2")
    output["negation_paraphrase_inversion"] = negative_material_perturbation(material_1, material_2, negative_paraphrase_comparison, premise_switch, "1")

    return output

def original_social_perturbation(situation, comparison_phrase, negation_switch, mode):
    negation_comparison_phrase = comparison_phrase.replace(negation_switch[mode][0], 
                                                           negation_switch[mode][1])

    a_position = situation.index("A")
    b_position = situation.index("B")

    flipped_situation = (situation[:a_position] + "B" + situation[a_position + 1:b_position] + 
                         "A" + situation[b_position+1:])
    
    original = situation + ", so A " + comparison_phrase + " B"
    asymmetric_premise = flipped_situation + ", so A " + negation_comparison_phrase + " B"
    asymmetric_conclusion = situation + ", so B " + negation_comparison_phrase + " A"

    return {"original" : original, "asymmetric_premise" : asymmetric_premise, "asymmetric_conclusion" : asymmetric_conclusion}

def negative_social_perturbation(situation, comparison_phrase, negation_switch, mode):
    negation_comparison_phrase = comparison_phrase.replace(negation_switch[mode][0], 
                                                           negation_switch[mode][1])

    a_position = situation.index("A")
    b_position = situation.index("B")

    flipped_situation = (situation[:a_position] + "B" + situation[a_position + 1:b_position] + 
                         "A" + situation[b_position+1:])

    original = situation + ", so A " + negation_comparison_phrase + " B"
    asymmetric_premise = flipped_situation + ", so A " + comparison_phrase + " B"
    asymmetric_conclusion = situation + ", so B " + comparison_phrase + " A"

    return {"original" : original, "asymmetric_premise" : asymmetric_premise, "asymmetric_conclusion" : asymmetric_conclusion}

def generate_social_perturbations(situation,
                                  negation_switch,
                                  antonym_switch,
                                  original_comparison,
                                  paraphrase,
                                  inverted_paraphrase,
                                  premise_switch):

    output = {}
    negative_comparison = original_comparison.replace(negation_switch["0"][0], negation_switch["0"][1])
    antonym_comparison = original_comparison.replace(antonym_switch[0], antonym_switch[1])
    negation_antonym_comparison = antonym_comparison.replace(negation_switch["0"][0], negation_switch["0"][1])

    negative_paraphrase_comparison = paraphrase.replace(negation_switch["1"][0], negation_switch["1"][1])
    negative_paraphrase_inversion_comparison = inverted_paraphrase.replace(negation_switch["2"][0], negation_switch["2"][1])

    output["original"] = original_social_perturbation(situation, original_comparison, premise_switch, "0")
    output["negation"] = negative_social_perturbation(situation, negative_comparison, premise_switch, "0")
    output["antonym"]  = negative_social_perturbation(situation, antonym_comparison, premise_switch, "0")
    output["paraphrase"] = original_social_perturbation(situation, paraphrase, premise_switch, "1")
    output["paraphrase_inversion"] = negative_social_perturbation(situation, inverted_paraphrase, premise_switch, "2")

    output["negation_antonym"] = original_social_perturbation(situation, negation_antonym_comparison, premise_switch, "0")
    output["negation_paraphrase"] = original_social_perturbation(situation, negative_paraphrase_inversion_comparison, premise_switch, "2")
    output["negation_paraphrase_inversion"] = negative_social_perturbation(situation, negative_paraphrase_comparison, premise_switch, "1")

    return output

    
   


    
