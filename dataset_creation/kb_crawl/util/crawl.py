from dataset_creation.kb_crawl.classes.static import Method, Comparison, Relation, POS
from dataset_creation.kb_crawl.classes.property import Property
from dataset_creation.kb_crawl.classes.logic import MaterialLogic
import dataset_creation.kb_crawl.conceptnet.api as cn_api

# Material_1, Material_2, Property Comparison
# Strategy: material → properties → property antonym → objects with property → made of 
def crawl_materials(materials: [(str, float)]) -> [MaterialLogic]:
  knowledge = []
  properties = {}

  for mat in materials:
    mat_1 = mat[0]
    threshold = mat[1]
    # extract properties
    # NOTE: specifying POS with HasProperty gives poor results
    mat_prop_res = cn_api.fetch(
      method=Method.Query,
      params=cn_api.build_params(start=mat_1, rel=Relation.HasProperty)
    )

    for prop_edge in mat_prop_res['edges']:
      prop_label = prop_edge['end']['label']
      mat_2 = set()
      prop = properties[prop_label] if prop_label in properties else None
      comp = Comparison.More
      weight = prop_edge['weight']
      
      # fetch antonym properties
      ant_query_params = cn_api.build_params_from_id(startId=prop_edge['end']['@id'], rel=Relation.Antonym, pos=POS.Adjective)
      ant_res = cn_api.fetch_with_cache(method=Method.Query, params=ant_query_params)

      if not ant_res:
        continue

      # insert into properties
      if not prop:
        prop = Property(prop_label, [ant_edge['end']['label'] for ant_edge in ant_res['edges']])
        properties[prop_label] = prop

      for ant_edge in ant_res['edges']:
        # fetch objects with antonym property
        obj_query_params = cn_api.build_params_from_id(endId=ant_edge['end']['@id'], rel=Relation.HasProperty)
        obj_res = cn_api.fetch_with_cache(method=Method.Query, params=obj_query_params)

        if not obj_res:
          continue

        for obj_edge in obj_res['edges']:
          # fech materials from objects
          mat_2_query_params = cn_api.build_params_from_id(startId=obj_edge['start']['@id'], rel=Relation.MadeOf)
          mat_2_res = cn_api.fetch_with_cache(method=Method.Query, params=mat_2_query_params)

          if not mat_2_res:
            continue

          # update materials
          mat_2.update([mat_2_edge['end']['label'] for mat_2_edge in mat_2_res['edges'] if (mat_2_edge['weight']*obj_edge['weight']*ant_edge['weight']*weight) > threshold])

      knowledge.append(MaterialLogic(mat_1, list(mat_2), prop, comp, weight))
    
  return knowledge

# Relation, Property_Comparison
# Strategy: Occupation/Role noun → capabilities
def crawl_relation():
  return 1

# Property, Property_Comparison
# Strategy: Action → property consequence → comparison
def crawl_property():
  return 1

# Property_Comparison, Property_Comparison
# Strategy: Action comparison → property consequence → action comparison
def crawl_comparison():
  return 1