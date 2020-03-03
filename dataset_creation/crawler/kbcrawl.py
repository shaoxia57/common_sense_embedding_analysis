import requests
from enum import Enum

# globals
cache = {}
base = 'http://api.conceptnet.io'
class Method(Enum):
  Assertion = 'a'
  Concept = 'c'
  Dataset = 'd'
  Relation = 'r'
  Source = 's'
  Conjunction = 'and'
  Related = 'related'
  Query = 'query'
class Language(Enum):
  English = 'en'
  French = 'fr'
  Italian = 'it'
  German = 'de'
  Spanish = 'es'
  Russian = 'ru'
  Portuguese = 'pt'
  Japanese = 'ja'
  Dutch = 'nl'
  Chinese = 'zh'
class Comparison(Enum):
  More = 1
  Equal = 0
  Less = -1
class Relation(Enum):
  RelatedTo = 'RelatedTo'
  FormOf = 'FormOf'
  IsA = 'IsA'
  PartOf = 'PartOf'
  HasA = 'HasA'
  UsedFor = 'UsedFor'
  CapableOf = 'CapableOf'
  AtLocation = 'AtLocation'
  Causes = 'Causes'
  HasSubevent = 'HasSubevent'
  HasFirstSubEvent = 'HasFirstSubEvent'
  HasLastSubevent = 'HasLastSubEvent'
  HasPrerequisite = 'HasPrerequisite'
  HasProperty = 'HasProperty'
  MotivatedByGoal = 'MotivatedByGoal'
  ObstructedBy = 'ObstructedBy'
  Desires = 'Desires'
  CreatedBy = 'CreatedBy'
  Synonym: 'Synonym'
  Antonym = 'Antonym'
  DistinctFrom = 'DistinctFrom'
  DerivedFrom = 'DerivedFrom'
  SymbolOf = 'SymbolOf'
  DefinedAs = 'DefinedAs'
  MannerOf = 'MannerOf'
  LocatedNear = 'LocatedNear'
  HasContext = 'HasContext'
  SimilarTo = 'SimilarTo'
  EtymologicallyRelatedTo = 'EtymologicallyRelatedTo'
  EtymologicallyDerivedFrom = 'EtymologicallyDerivedFrom'
  CausesDesire = 'CausesDesire'
  MadeOf = 'MadeOf'
  ReceivesAction = 'ReceivesAction'
  ExternalURL = 'ExternalURL'
class POS(Enum):
  Noun = 'n'
  Verb = 'v'
  Adjective = 'a'
  AdjectiveSatellite = 's'
  Adverb = 'r'

# fetches a conceptnet query
def fetch(query: str = None, language: Language = Language.English, method: Method = Method.Concept, params: dict = None, pos: POS = None) -> dict:
  if method is not Method.Query:
    url = '/'.join(filter(None, [base, method.value, language.value, query, pos]))
  else:
    url = '/'.join([base, method.value])
  return requests.get(url, params).json()

def fetch_with_cache(query: str = None, language: Language = Language.English, method: Method = Method.Concept, params: dict = None, pos: POS = None):
  res_id = build_query_id(params)
  if res_id in cache:
    # hit
    return cache[res_id]
  else:
    # miss
    res = fetch(
      query=query,
      language=language,
      method=method,
      params=params,
      pos=pos
    )
    cache[res['@id']] = res
    return res

def build_params(start: str = None, end: str = None, rel: Relation = None, node: str = None, other: str = None, language: Language = Language.English, pos: POS = None, limit: int = 1000):
  nodeURI = '/' + '/'.join([Method.Concept.value, language.value])
  relURI = '/' + Method.Relation.value
  pos=pos.value if pos else None
  params = {
    'start': '/'.join(filter(None, [nodeURI, start, pos])) if start else None,
    'end': '/'.join(filter(None, [nodeURI, end, pos])) if end else None,
    'rel': '/'.join([relURI, rel.value]) if rel else None,
    'node': '/'.join(filter(None, [nodeURI, node, pos])) if node else None,
    'other': '/'.join(filter(None, [nodeURI, other, pos])) if other else None,
    'limit': limit
  }
  return params

def build_params_from_id(startId: str = None, endId: str = None, rel: Relation = None, nodeId: str = None, otherId: str = None, pos: POS = None, limit: int = 1000):
  relURI = '/' + Method.Relation.value
  pos=pos.value if pos else None
  params = {
    'start': '/'.join(filter(None, [startId, pos])) if startId else None,
    'end': '/'.join(filter(None, [endId, pos])) if endId else None,
    'rel': '/'.join([relURI, rel.value]) if rel else None,
    'node': '/'.join(filter(None, [nodeId, pos])) if nodeId else None,
    'other': '/'.join(filter(None, [otherId, pos])) if otherId else None,
    'limit': limit
  }
  return params

# specifically for Method.Query
# TODO: make more general
def build_query_id(params: dict):
  del params['limit']
  queryURI = '/' + Method.Query.value
  params = '&'.join([key + '=' + str(val) for (key, val) in sorted(params.items()) if val])
  return queryURI + ('?' + params) if params else ''

class Property:
  def __init__(self, original: str, antonym: [str] = [], paraphrase: [str] = []):
    self.original = original
    self.antonym = antonym
    self.paraphrase = paraphrase

# Material_1, Material_2, Property Comparison
# Strategy: material → properties → property antonym → materials with property
class MaterialLogic:
  def __init__(self, mat_1: str, mat_2: [str], prop: Property, comp: Comparison = Comparison.More, weight: float = 1.0):
    self.mat_1 = mat_1
    self.mat_2 = mat_2
    self.prop = prop
    self.comp = comp
    self.weight = weight

def crawl_materials(materials: [str], threshold = 1.0) -> [MaterialLogic]:
  knowledge = []
  properties = {}

  for mat_1 in materials:
    # extract properties
    # NOTE: specifying POS with HasProperty gives poor results
    mat_prop_res = fetch(
      method=Method.Query,
      params=build_params(start=mat_1, rel=Relation.HasProperty)
    )

    for prop_edge in mat_prop_res['edges']:
      prop_label = prop_edge['end']['label']
      mat_2 = set()
      prop = properties[prop_label] if prop_label in properties else None
      comp = Comparison.More
      weight = prop_edge['weight']
      
      # fetch antonym properties
      ant_query_params = build_params_from_id(startId=prop_edge['end']['@id'], rel=Relation.Antonym, pos=POS.Adjective)
      ant_res = fetch_with_cache(method=Method.Query, params=ant_query_params)

      # insert into properties
      if not prop:
        prop = Property(prop_label, [ant_edge['end']['label'] for ant_edge in ant_res['edges']])
        properties[prop_label] = prop

      for ant_edge in ant_res['edges']:
        # fetch materials with antonym property
        mat_2_query_params = build_params_from_id(endId=ant_edge['end']['@id'], rel=Relation.HasProperty)
        mat_2_res = fetch_with_cache(method=Method.Query, params=mat_2_query_params)

        # update materials
        mat_2.update([mat_2_edge['start']['label'] for mat_2_edge in mat_2_res['edges'] if (mat_2_edge['weight']*ant_edge['weight']*weight) > threshold])

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