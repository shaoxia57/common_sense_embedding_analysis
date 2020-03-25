from dataset_creation.kb_crawl.classes.static import Method, Comparison, Relation, POS, CometRelation
from dataset_creation.kb_crawl.classes.property import Property
from dataset_creation.kb_crawl.classes.logic import MaterialLogic, RelationLogic

import dataset_creation.kb_crawl.conceptnet.api as cn_api
from dataset_creation.kb_crawl.comet.conceptnet_api import CometModel

comet_conceptnet_model = 'dataset_creation/kb_crawl/comet/pretrained_models/conceptnet_pretrained_model.pickle'

class Crawler:
  def __init__(self, device=0):
    self.device = device
    self.cn_api = cn_api

    print(f'Initializing comet model from: {comet_conceptnet_model}')
    self.comet_cn_api = CometModel(device, model_file=comet_conceptnet_model)

  def comet_interact(self):
    self.comet_cn_api.interact()

  # Material_1, Material_2, Property Comparison
  # Strategy: material → properties (comet) → property antonym (cn) → materials made of property antonym (comet)
  def crawl_comet_materials(self, materials, topK=10):
    # Material_1, Material_2, Property Comparison
    # Strategy: material → properties → antonym properties → objects made of
    knowledge = []
    properties = {}

    for mat_1 in materials:
      mat_1_relations = ['HasProperty']

      # fetch material properties
      prop_outputs = self.comet_cn_api.query(mat_1, mat_1_relations, 'beam', topK)

      for mat_1_rel in mat_1_relations: 
        prop_output = prop_outputs[mat_1_rel]
        for prop_count, prop_label in enumerate(prop_output['beams']):
          mat_2 = set()
          prop = properties[prop_label] if prop_label in properties else None
          comp = Comparison.More
          weight = prop_count
          
          # fetch antonym properties from conceptnet
          ant_query_params = cn_api.build_params(start=prop_label, rel=Relation.Antonym, pos=POS.Adjective, limit=topK)
          ant_res = cn_api.fetch_with_cache(method=Method.Query, params=ant_query_params)

          if not ant_res:
            continue

          # insert into properties
          if not prop:
            prop = Property(prop_label, [ant_edge['end']['label'] for ant_edge in ant_res['edges']])
            properties[prop_label] = prop

          for ant_edge in ant_res['edges']:
            ant = ant_edge['end']['label']

            # fetch made of objects
            ant_relations = ['MadeOf']
            mat_2_outputs = self.comet_cn_api.query(ant, ant_relations, 'beam', topK)
            
            for prop_rel in ant_relations:
              mat_2_output = mat_2_outputs[prop_rel]
              mat_2.update(mat_2_output['beams'])
          
          knowledge.append(MaterialLogic(mat_1, list(mat_2), prop, comp, weight))

    return knowledge  

  # Material_1, Material_2, Property Comparison
  # Strategy: material → properties (cn) → property antonym (cn) → materials made of property antonym (comet)
  def crawl_materials(self, materials: [str], topK: int = 10, threshold: float = 0) -> [MaterialLogic]:
    knowledge = []
    properties = {}

    for mat_1 in materials:
      # extract properties from conceptnet
      # NOTE: specifying POS with HasProperty gives poor results
      mat_prop_res = cn_api.fetch(
        method=Method.Query,
        params=cn_api.build_params(start=mat_1, rel=Relation.HasProperty, limit=topK)
      )

      for prop_edge in mat_prop_res['edges']:
        prop_label = prop_edge['end']['label']
        mat_2 = set()
        prop = properties[prop_label] if prop_label in properties else None
        comp = Comparison.More
        weight = prop_edge['weight']
        
        # fetch antonym properties from conceptnet
        ant_query_params = cn_api.build_params_from_id(startId=prop_edge['end']['@id'], rel=Relation.Antonym, pos=POS.Adjective, limit=topK)
        ant_res = cn_api.fetch_with_cache(method=Method.Query, params=ant_query_params)

        if not ant_res:
          continue

        # insert into properties
        if not prop:
          prop = Property(prop_label, [ant_edge['end']['label'] for ant_edge in ant_res['edges']])
          properties[prop_label] = prop

        for ant_edge in ant_res['edges']:
          ant = ant_edge['end']['label']

          # fetch materials with property from comet
          ant_relations = ['MadeOf']
          mat_2_outputs = self.comet_cn_api.query(ant, ant_relations, 'beam', topK)
          
          for ant_rel in ant_relations:
            mat_2_output = mat_2_outputs[ant_rel]
            mat_2.update(mat_2_output['beams'])
          
        knowledge.append(MaterialLogic(mat_1, list(mat_2), prop, comp, weight))

        # for ant_edge in ant_res['edges']:
        #   # fetch objects with antonym property
        #   obj_query_params = cn_api.build_params_from_id(endId=ant_edge['end']['@id'], rel=Relation.HasProperty, limit=topK)
        #   obj_res = cn_api.fetch_with_cache(method=Method.Query, params=obj_query_params)

        #   if not obj_res:
        #     continue

        #   for obj_edge in obj_res['edges']:
        #     # fech materials from objects
        #     mat_2_query_params = cn_api.build_params_from_id(startId=obj_edge['start']['@id'], rel=Relation.MadeOf, limit=topK)
        #     mat_2_res = cn_api.fetch_with_cache(method=Method.Query, params=mat_2_query_params)

        #     if not mat_2_res:
        #       continue

        #     # update materials
        #     mat_2.update([mat_2_edge['end']['label'] for mat_2_edge in mat_2_res['edges'] if (mat_2_edge['weight']*obj_edge['weight']*ant_edge['weight']*weight) > threshold])

        # knowledge.append(MaterialLogic(mat_1, list(mat_2), prop, comp, weight))
      
    return knowledge

  # Relation, Property_Comparison
  # Strategy: Occupation/Role noun → capabilities
  def crawl_relations(self, relations: [str], topK: int = 10):
    knowledge = []
    properties = {}
    
    for relation in relations:
      relation_relations = ['CapableOf']
      capability_outputs = self.comet_cn_api.query(relation, relation_relations, 'beam', topK)

      for relation_rel in relation_relations: 
        capability_output = capability_outputs[relation_rel]
        for capability_count, capability_label in enumerate(capability_output['beams']):
          prop = properties[capability_label] if capability_label in properties else None
          comp = Comparison.More
          weight = capability_count

          # insert into properties
          if not prop:
            # fetch antonym properties from conceptnet
            ant_query_params = cn_api.build_params(start=capability_label, rel=Relation.Antonym, limit=topK)
            ant_res = cn_api.fetch_with_cache(method=Method.Query, params=ant_query_params)
            ants = [ant_edge['end']['label'] for ant_edge in ant_res['edges']] if ant_res else []
            prop = Property(capability_label, ants)
            properties[capability_label] = prop

          knowledge.append(RelationLogic(relation, prop, comp, weight))

    return knowledge

  # Property, Property_Comparison
  # Strategy: Action → property consequence → comparison
  def crawl_properties(self, properties: [str], topK: int = 10):
    return 1

  # Property_Comparison, Property_Comparison
  # Strategy: Action comparison → property consequence → action comparison
  def crawl_comparisons(self, comparisons: [str], topK: int = 10):
    return 1