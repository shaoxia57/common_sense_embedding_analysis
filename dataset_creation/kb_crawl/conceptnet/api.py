import requests
import json

from dataset_creation.kb_crawl.classes.static import Method, Language, Comparison, Relation, POS

# globals
base = 'http://api.conceptnet.io'
cache = {}

# fetches a conceptnet query
def fetch(query: str = None, language: Language = Language.English, method: Method = Method.Concept, params: dict = None, pos: POS = None) -> dict:
  if method is not Method.Query:
    url = '/'.join(filter(None, [base, method.value, language.value, query, pos]))
  else:
    url = '/'.join([base, method.value])
  try:
    return requests.get(url, params).json()
  except requests.exceptions.Timeout:
    print(f'Error encountered during fetch: timeout')
    return None
  except requests.exceptions.RequestException as e:
    print(f'Error encountered during fetch: {e}')
    return None
  except json.decoder.JSONDecodeError as e:
    print(f'Error encountered during JSON decoding: {e}')
    return None
  
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
    if res:
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