from dataset_creation.kb_crawl.classes.word import Word

class Comparison:
  def __init__(self, original: Word, negation: Word = None, paraphrase: [Word] = []):
    self.original = original
    self.negation = negation
    self.paraphrase = paraphrase