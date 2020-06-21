import sys
import os

sys.path.append(os.getcwd())

import utils.io as io
from dataset_creation.kb_crawl.crawler.crawler import Crawler

if __name__ == "__main__":
  crawlSettings = {
    'material': True,
    'relation': True,
    'property': False,
    'comparison': False,
  }
  crawler = Crawler()

  # crawler.comet_conceptnet_interact()
  # crawler.comet_atomic_interact()

  if crawlSettings['material']:
    materials = io.read_file('example_materials_input.csv')

    print('Generating Conceptnet Materials...')
    materials_knowledge1 = crawler.crawl_materials(materials)
    io.write_materials('example_materials_output.csv', materials_knowledge1)

    print('Generating Comet Conceptnet Materials...')
    materials_knowledge2 = crawler.crawl_comet_materials(materials)
    io.write_materials('example_comet_materials_output.csv', materials_knowledge2)

  if crawlSettings['relation']:
    relations = io.read_file('example_relations_input.csv')

    print('Generating Relations...')
    relations_knowledge = crawler.crawl_relations(relations)
    io.write_relations('example_relations_output.csv', relations_knowledge)

  if crawlSettings['property']:
    properties = io.read_file('example_properties_input.csv')

    print('Generating Properties...')
    properties_knowledge = crawler.crawl_properties(properties)
    io.write_relations('example_properties_output.csv', properties_knowledge)

  if crawlSettings['comparison']:
    comparisons = io.read_file('example_comparisons_input.csv')

    print('Generating Comparisons...')
    comparisons_knowledge = crawler.crawl_comparisons(comparisons)
    io.write_comparisons('example_comparisons_output.csv', comparisons_knowledge)