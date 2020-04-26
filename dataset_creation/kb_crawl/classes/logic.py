from dataset_creation.kb_crawl.classes.word import Word
from dataset_creation.kb_crawl.classes.comparison import Comparison
from dataset_creation.kb_crawl.classes.property import Property
class MaterialLogic:
  def __init__(self, mat_1: Word, mat_2: [Word], prop: Property, comp: Comparison = Comparison(Word('more'), Word('less')), weight: float = 1.0):
    self.mat_1 = mat_1
    self.mat_2 = mat_2
    self.prop = prop
    self.comp = comp
    self.weight = weight

class RelationLogic:
  def __init__(self, relation: Word, prop: Property, comp: Comparison = Comparison(Word('more'), Word('less')), weight: float = 1.0):
    self.relation = relation
    self.prop = prop
    self.comp = comp
    self.weight = weight