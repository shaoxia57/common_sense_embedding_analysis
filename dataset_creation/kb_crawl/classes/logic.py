from dataset_creation.kb_crawl.classes.property import Property
from dataset_creation.kb_crawl.classes.static import Comparison

class MaterialLogic:
  def __init__(self, mat_1: str, mat_2: [str], prop: Property, comp: Comparison = Comparison.More, weight: float = 1.0):
    self.mat_1 = mat_1
    self.mat_2 = mat_2
    self.prop = prop
    self.comp = comp
    self.weight = weight

class RelationLogic:
  def __init__(self, relation: str, prop: Property, comp: Comparison = Comparison.More, weight: float = 1.0):
    self.relation = relation
    self.prop = prop
    self.comp = comp
    self.weight = weight