from dataset_creation.kb_crawl.classes.static import Method, Relation, POS, CometRelation
from dataset_creation.kb_crawl.classes.word import Word
from dataset_creation.kb_crawl.classes.comparison import Comparison
from dataset_creation.kb_crawl.classes.property import Property
from dataset_creation.kb_crawl.classes.logic import MaterialLogic, RelationLogic

import dataset_creation.kb_crawl.utils.conceptnet as Conceptnet
from dataset_creation.kb_crawl.utils.comet_transformers import CometConceptnetModel
from dataset_creation.kb_crawl.utils.comet_transformers import CometAtomicModel

comet_conceptnet_model = 'dataset_creation/kb_crawl/comet/pretrained_models/conceptnet_pretrained_model.pickle'
comet_atomic_model = 'dataset_creation/kb_crawl/comet/pretrained_models/atomic_pretrained_model.pickle'
class Crawler:
  def __init__(self, device=0):
    self.device = device

    print(f'Initializing comet conceptnet model from: {comet_conceptnet_model}')
    self.comet_conceptnet_model = CometConceptnetModel(device, model_file=comet_conceptnet_model)

    print(f'Initializing comet atomic model from: {comet_atomic_model}')
    self.comet_atomic_model = CometAtomicModel(device, model_file=comet_atomic_model)

  def comet_conceptnet_interact(self):
    self.comet_conceptnet_model.interact()

  def comet_atomic_interact(self):
    self.comet_atomic_model.interact()

  # Material_1, Material_2, Property Comparison
  # Strategy: material → properties (comet) → property antonym (cn) → materials made of property antonym (comet)
  def crawl_comet_materials(self, materials, sampler = 'topk', samples = 10):
    knowledge = []
    prop_dict = {}

    # common comparisons
    comp_more = Comparison(Word('more', self.comet_conceptnet_model.encode('more')), Word('less', self.comet_conceptnet_model.encode('less')))

    for mat_1 in materials:
      mat_1_relations = ['HasProperty']

      # fetch material properties
      prop_outputs = self.comet_conceptnet_model.query(mat_1, mat_1_relations, sampler, samples)

      for mat_1_rel in mat_1_relations: 
        prop_output = prop_outputs[mat_1_rel]
        for prop_i, prop_label in enumerate(prop_output['beams']):
          mat_2_dict = {}
          prop = prop_dict[prop_label] if prop_label in prop_dict else None
          comp = comp_more
          weight = prop_i
          
          # fetch antonym properties from conceptnet
          ant_query_params = Conceptnet.build_params(start=prop_label, rel=Relation.Antonym, pos=POS.Adjective, limit=samples)
          ant_res = Conceptnet.fetch_with_cache(method=Method.Query, params=ant_query_params)

          if not ant_res:
            continue

          # insert into properties
          if not prop:
            prop = Property(
              Word(prop_label, prop_output['tokens'][prop_i]), 
              [Word(ant_edge['end']['label'], self.comet_conceptnet_model.encode(ant_edge['end']['label'])) for ant_edge in ant_res['edges']]
            )
            prop_dict[prop_label] = prop

          for ant_edge in ant_res['edges']:
            ant = ant_edge['end']['label']

            # fetch made of objects
            ant_relations = ['MadeOf']
            mat_2_outputs = self.comet_conceptnet_model.query(ant, ant_relations, sampler, samples)
            
            for prop_rel in ant_relations:
              mat_2_output = mat_2_outputs[prop_rel]
              for mat_2_i, mat_2 in enumerate(mat_2_output['beams']):
                if mat_2 not in mat_2_dict:
                  mat_2_dict[mat_2] = mat_2_output['tokens'][mat_2_i]
          
          # make words
          mat_2_words = []
          for mat_2 in mat_2_dict:
            mat_2_words.append(Word(mat_2, mat_2_dict[mat_2]))

          material_logic = MaterialLogic(
            Word(mat_1, prop_output['input_token']),
            mat_2_words, 
            prop, 
            comp, 
            weight
          )

          knowledge.append(material_logic)

    return knowledge  

  # Material_1, Material_2, Property Comparison
  # Strategy: material → properties (cn) → property antonym (cn) → materials made of property antonym (comet)
  def crawl_materials(self, materials: [str], sampler: str = 'topk', samples: int = 10, threshold: float = 0) -> [MaterialLogic]:
    knowledge = []
    prop_dict = {}

    # common comparisons
    comp_more = Comparison(Word('more', self.comet_conceptnet_model.encode('more')), Word('less', self.comet_conceptnet_model.encode('less')))

    for mat_1 in materials:
      # extract properties from conceptnet
      # NOTE: specifying POS with HasProperty gives poor results
      mat_prop_res = Conceptnet.fetch(
        method=Method.Query,
        params=Conceptnet.build_params(start=mat_1, rel=Relation.HasProperty, limit=samples)
      )

      for prop_edge in mat_prop_res['edges']:
        prop_label = prop_edge['end']['label']
        mat_2_dict = {}
        prop = prop_dict[prop_label] if prop_label in prop_dict else None
        comp = comp_more
        weight = prop_edge['weight']
        
        # fetch antonym properties from conceptnet
        ant_query_params = Conceptnet.build_params_from_id(startId=prop_edge['end']['@id'], rel=Relation.Antonym, pos=POS.Adjective, limit=samples)
        ant_res = Conceptnet.fetch_with_cache(method=Method.Query, params=ant_query_params)

        if not ant_res:
          continue

        # insert into properties
        if not prop:
          prop = Property(
            Word(prop_label, self.comet_conceptnet_model.encode(prop_label)), 
            [Word(ant_edge['end']['label'], self.comet_conceptnet_model.encode(ant_edge['end']['label'])) for ant_edge in ant_res['edges']]
          )
          prop_dict[prop_label] = prop

        for ant_edge in ant_res['edges']:
          ant = ant_edge['end']['label']

          # fetch materials with property from comet
          ant_relations = ['MadeOf']
          mat_2_outputs = self.comet_conceptnet_model.query(ant, ant_relations, sampler, samples)
          
          for ant_rel in ant_relations:
            mat_2_output = mat_2_outputs[ant_rel]
            for mat_2_i, mat_2 in enumerate(mat_2_output['beams']):
              mat_2_dict[mat_2] = mat_2_output['tokens'][mat_2_i]
        
        # make words
        mat_2_words = []
        for mat_2 in mat_2_dict:
          mat_2_words.append(Word(mat_2, mat_2_dict[mat_2]))

        material_logic = MaterialLogic(
          Word(mat_1, self.comet_conceptnet_model.encode(mat_1)),
          mat_2_words, 
          prop, 
          comp, 
          weight
        )

        knowledge.append(material_logic)
  
    return knowledge

  # Relation, Property_Comparison
  # Strategy: Occupation/Role noun → capabilities
  def crawl_relations(self, relations: [str], sampler = 'topk', samples: int = 10):
    knowledge = []
    prop_dict = {}

    # common comparisons
    comp_more = Comparison(Word('more', self.comet_conceptnet_model.encode('more')), Word('less', self.comet_conceptnet_model.encode('less')))
    
    for relation in relations:
      relation_relations = ['CapableOf']
      capability_outputs = self.comet_conceptnet_model.query(relation, relation_relations, sampler, samples)

      for relation_rel in relation_relations: 
        capability_output = capability_outputs[relation_rel]
        for capability_i, capability_label in enumerate(capability_output['beams']):
          prop = prop_dict[capability_label] if capability_label in prop_dict else None
          comp = comp_more
          weight = capability_i

          # insert into properties
          if not prop:
            # fetch antonym properties from conceptnet
            ant_query_params = Conceptnet.build_params(start=capability_label, rel=Relation.Antonym, limit=samples)
            ant_res = Conceptnet.fetch_with_cache(method=Method.Query, params=ant_query_params)
            prop = Property(
              Word(capability_label, capability_output['tokens'][capability_i]), 
              [Word(ant_edge['end']['label'], self.comet_conceptnet_model.encode(ant_edge['end']['label'])) for ant_edge in ant_res['edges']] if ant_res else [])
            prop_dict[capability_label] = prop

          relation_logic = RelationLogic(
            Word(relation, capability_output['input_token']),
            prop,
            comp,
            weight
          )

          knowledge.append(relation_logic)

    return knowledge

  # Property, Property_Comparison
  # Strategy: Action → property consequence → comparison
  def crawl_properties(self, properties: [str], topK: int = 10):
    return 1

  # Property_Comparison, Property_Comparison
  # Strategy: Action comparison → property consequence → action comparison
  def crawl_comparisons(self, comparisons: [str], topK: int = 10):
    return 1