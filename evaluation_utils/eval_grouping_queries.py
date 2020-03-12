import pandasql as ps
def run_template_seperate_operator_grouping_query(df):
    template_seperate_operator_grouping_query = """
                                                    SELECT template, 
                                                           linguistic_operator, 
                                                           asymetric_operator, 
                                                           AVG(stat) AS avg_stat
                                                    FROM df
                                                    GROUP BY template, 
                                                             linguistic_operator, 
                                                             asymetric_operator
                                                    ORDER by template ASC
                                                """
    result = ps.sqldf(template_seperate_operator_grouping_query, locals())
    return result


def run_template_merged_operator_grouping_query(df):
    template_merged_operator_grouping_query = """
                                                  SELECT template, 
                                                         perturbation, 
                                                         AVG(stat) AS avg_stat
                                                  FROM df
                                                  GROUP BY template, 
                                                           perturbation
                                                  ORDER by template ASC
                                              """
    result = ps.sqldf(template_merged_operator_grouping_query, locals())
    return result

def run_set_merged_operator_grouping_query(df):
    set_joined_operator_grouping_query = """
                                             SELECT set_number,
                                                    perturbation, 
                                                    AVG(stat) AS avg_stat
                                             FROM df
                                             GROUP BY set_number,
                                                      perturbation
                                             ORDER by set_number ASC
                                         """
    result = ps.sqldf(set_joined_operator_grouping_query, locals())
    return result

def run_template_grouping_query(df):
    template_grouping_query = """
                                  SELECT template, 
                                         AVG(stat) AS avg_stat, 
                                         COUNT(1) as count
                                  FROM df
                                  GROUP BY template
                                  ORDER by template
                              """
    result = ps.sqldf(template_grouping_query, locals())
    return result

def run_set_grouping_query(df):
    template_grouping_query = """
                                  SELECT set_number, 
                                         AVG(stat) AS avg_stat, 
                                         COUNT(1) as count
                                  FROM df
                                  GROUP BY set_number
                                  ORDER by set_number
                              """
    result = ps.sqldf(template_grouping_query, locals())
    return result

def run_perturbation_grouping_query(df):
    perturbation_grouping_query = """
                                      SELECT perturbation, 
                                             AVG(stat) AS avg_stat, 
                                             COUNT(1) as count
                                      FROM df
                                      GROUP BY perturbation
                                      ORDER by CASE WHEN perturbation LIKE 'original%' THEN '1'
                                                    WHEN perturbation LIKE 'negation%' THEN '2'
                                                    WHEN perturbation LIKE 'antonym%' THEN '3'
                                                    WHEN perturbation LIKE 'paraphrase%' THEN '4'
                                                    WHEN perturbation LIKE 'paraphrase_inversion%' THEN '5'
                                                    WHEN perturbation LIKE 'negation_antonym%' THEN '6'
                                                    WHEN perturbation LIKE 'negation_paraphrase%' THEN '7'
                                                    WHEN perturbation LIKE 'negation_paraphrase_inversion%' THEN '8'
                                                    END
                                  """
    result = ps.sqldf(perturbation_grouping_query, locals())
    return result

def run_linguistic_operator_grouping_query(df):
    linguistic_operator_grouping_query = """
                                             SELECT linguistic_operator, 
                                                    AVG(stat) AS avg_stat, 
                                                    COUNT(1) as count
                                             FROM df
                                             WHERE asymetric_operator = "original"
                                             GROUP BY linguistic_operator
                                             ORDER by CASE WHEN linguistic_operator LIKE 'original' THEN '1'
                                                           WHEN linguistic_operator LIKE 'negation_antonym' THEN '6'
                                                           WHEN linguistic_operator LIKE 'negation_paraphrase' THEN '7'
                                                           WHEN linguistic_operator LIKE 'negation_paraphrase_inversion' THEN '8'
                                                           WHEN linguistic_operator LIKE 'negation' THEN '2'
                                                           WHEN linguistic_operator LIKE 'antonym' THEN '3'
                                                           WHEN linguistic_operator LIKE 'paraphrase_inversion' THEN '5'
                                                           WHEN linguistic_operator LIKE 'paraphrase' THEN '4'
                                                           END
                                         """
    result = ps.sqldf(linguistic_operator_grouping_query, locals())
    return result

def run_asymetric_operator_grouping_query(df):
    asymetric_operator_grouping_query = """
                                             SELECT asymetric_operator, 
                                                    AVG(stat) AS avg_stat, 
                                                    COUNT(1) as count
                                             FROM df
                                             GROUP BY asymetric_operator
                                             ORDER by CASE WHEN asymetric_operator LIKE 'original' THEN '1'
                                                           WHEN asymetric_operator LIKE 'asymmetric_premise' THEN '2'
                                                           WHEN asymetric_operator LIKE 'negation_paraphrase%' THEN '3'
                                                           END
                                         """
    result = ps.sqldf(asymetric_operator_grouping_query, locals())
    return result
