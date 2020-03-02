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


