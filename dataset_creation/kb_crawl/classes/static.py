from enum import Enum

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

  
# Method = {
#   'Assertion': 'a',
#   'Concept': 'c',
#   'Dataset': 'd',
#   'Relation': 'r',
#   'Source': 's',
#   'Conjunction': 'and',
#   'Related': 'related',
#   'Query': 'query'
# }
# Language = {
#   'English': 'en',
#   'French': 'fr',
#   'Italian': 'it',
#   'German': 'de',
#   'Spanish': 'es',
#   'Russian': 'ru',
#   'Portuguese': 'pt',
#   'Japanese': 'ja',
#   'Dutch': 'nl',
#   'Chinese': 'zh'
# }
# Comparison = {
#   'More': 'more',
#   'Equal': 'equal',
#   'Less': 'less,'
# }
# Relation = {
#   'RelatedTo': 'RelatedTo',
#   'FormOf': 'FormOf',
#   'IsA': 'IsA',
#   'PartOf': 'PartOf',
#   'HasA': 'HasA',
#   'UsedFor': 'UsedFor',
#   'CapableOf': 'CapableOf',
#   'AtLocation': 'AtLocation',
#   'Causes': 'Causes',
#   'HasSubevent': 'HasSubevent',
#   'HasFirstSubEvent': 'HasFirstSubEvent',
#   'HasLastSubevent': 'HasLastSubEvent',
#   'HasPrerequisite': 'HasPrerequisite',
#   'HasProperty': 'HasProperty',
#   'MotivatedByGoal': 'MotivatedByGoal',
#   'ObstructedBy': 'ObstructedBy',
#   'Desires': 'Desires',
#   'CreatedBy': 'CreatedBy',
#   'Synonym': 'Synonym',
#   'Antonym': 'Antonym',
#   'DistinctFrom': 'DistinctFrom',
#   'DerivedFrom': 'DerivedFrom',
#   'SymbolOf': 'SymbolOf',
#   'DefinedAs': 'DefinedAs',
#   'MannerOf': 'MannerOf',
#   'LocatedNear': 'LocatedNear',
#   'HasContext': 'HasContext',
#   'SimilarTo': 'SimilarTo',
#   'EtymologicallyRelatedTo': 'EtymologicallyRelatedTo',
#   'EtymologicallyDerivedFrom': 'EtymologicallyDerivedFrom',
#   'CausesDesire': 'CausesDesire',
#   'MadeOf': 'MadeOf',
#   'ReceivesAction': 'ReceivesAction',
#   'ExternalURL': 'ExternalURL'
# }
# POS = {
#   'Noun': 'n',
#   'Verb': 'v',
#   'Adjective': 'a',
#   'AdjectiveSatellite': 's',
#   'Adverb': 'r',
# }
