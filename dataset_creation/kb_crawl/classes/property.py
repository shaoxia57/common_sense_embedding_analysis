from dataset_creation.kb_crawl.classes.word import Word

class Property:
  def __init__(self, original: Word, antonym: [Word] = [], paraphrase: [Word] = []):
    self.original = original
    self.antonym = antonym
    self.paraphrase = paraphrase