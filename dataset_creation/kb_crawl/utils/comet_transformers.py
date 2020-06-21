import os
import sys
import argparse
import torch

import dataset_creation.kb_crawl.comet.src.data.data as data
import dataset_creation.kb_crawl.comet.src.data.config as cfg
import dataset_creation.kb_crawl.comet.src.api as api

conceptnet_pretrained_file = 'dataset_creation/kb_crawl/comet/pretrained_models/conceptnet_pretrained_model.pickle'
atomic_pretrained_file = 'dataset_creation/kb_crawl/comet/pretrained_models/atomic_pretrained_model.pickle'

class CometConceptnetModel:
  def __init__(self, device='cpu', model_file=conceptnet_pretrained_file):
    self.device = device
    self.model_file = model_file
    
    # setup
    self.opt, self.state_dict = api.load_model_file(self.model_file)

    self.data_loader, self.text_encoder = api.load_data('conceptnet', self.opt)

    n_ctx = self.data_loader.max_e1 + self.data_loader.max_e2 + self.data_loader.max_r
    n_vocab = len(self.text_encoder.encoder) + n_ctx

    self.model = api.make_model(self.opt, n_vocab, n_ctx, self.state_dict)

    if self.device != 'cpu':
      cfg.device = int(self.device)
      cfg.do_gpu = True
      torch.cuda.set_device(cfg.device)
      self.model.cuda(cfg.device)
    else:
      cfg.device = 'cpu'  
    
  def query(self, query, relations, sampling_algorithm='beam', search_size=10):
    sampler = api.set_sampler(self.opt, sampling_algorithm, search_size, self.data_loader)  
    return api.get_conceptnet_sequence(
      query, 
      self.model, 
      sampler, 
      self.data_loader, 
      self.text_encoder, 
      relations
    )

  def encode(self, target):
    return self.text_encoder.encode([target], verbose=False)[0]

  def interact(self):
    while True:
      query = 'help'
      relation = 'help'
      sampling_method = 'help'

      while query is None or query.lower() == 'help':
        query = input('Give an input entity (e.g., go on a hike -- works best if words are lemmatized): ')

        if query == 'help':
          api.print_help(self.opt.dataset)
          
      if query == 'quit':
        break

      while relation.lower() == 'help':
        relation = input('Give a relation (type \'help\' for an explanation): ')

        if relation == 'help':
          api.print_relation_help(self.opt.dataset)

      while sampling_method.lower() == 'help':
        sampling_method = input('Give a sampling algorithm (type \'help\' for an explanation): ')

        if sampling_method == 'help':
            api.print_sampling_help()

      sampling_method_split = sampling_method.split('-')
      sampling_algorithm = str(sampling_method_split[0])
      search_size = int(sampling_method_split[1]) if len(sampling_method_split) > 1 else 10

      sampler = api.set_sampler(self.opt, sampling_algorithm, search_size, self.data_loader)

      if relation not in data.conceptnet_data.conceptnet_relations:
        relation = 'all'

      outputs = api.get_conceptnet_sequence(
        query, self.model, sampler, self.data_loader, self.text_encoder, relation, print=True)

class CometAtomicModel:
  def __init__(self, device='cpu', model_file=atomic_pretrained_file):
    self.device = device
    self.model_file = model_file

    # setup
    self.opt, self.state_dict = api.load_model_file(self.model_file)

    self.data_loader, self.text_encoder = api.load_data('atomic', self.opt)

    n_ctx = self.data_loader.max_event + self.data_loader.max_effect
    n_vocab = len(self.text_encoder.encoder) + n_ctx

    self.model = api.make_model(self.opt, n_vocab, n_ctx, self.state_dict)

    if self.device != 'cpu':
      cfg.device = int(self.device)
      cfg.do_gpu = True
      torch.cuda.set_device(cfg.device)
      self.model.cuda(cfg.device)
    else:
      cfg.device = 'cpu'

  def query(self, query, category, sampling_algorithm='beam', search_size=10):
    sampler = api.set_sampler(self.opt, sampling_algorithm, search_size, self.data_loader)
    return api.get_atomic_sequence(
      query, 
      self.model, 
      sampler, 
      self.data_loader, 
      self.text_encoder, 
      category
    )

  def encode(self, target):
    return self.text_encoder.encode([target], verbose=False)[0]
  
  def interact(self):
    while True:
      query = 'help'
      category = 'help'
      sampling_method = 'help'

      while query is None or query.lower() == 'help':
        query = input('Give an event (e.g., PersonX went to the mall): ')

        if query == 'help':
            api.print_help(self.opt.dataset)
          
      if query == 'quit':
        break

      while category.lower() == 'help':
        category = input('Give an effect type (type \'help\' for an explanation): ')

        if category == 'help':
          api.print_category_help(self.opt.dataset)

      while sampling_method.lower() == 'help':
        sampling_method = input('Give a sampling algorithm (type \'help\' for an explanation): ')

        if sampling_method == 'help':
            api.print_sampling_help()

      sampling_method_split = sampling_method.split('-')
      sampling_algorithm = str(sampling_method_split[0])
      search_size = int(sampling_method_split[1]) if len(sampling_method_split) > 1 else 10

      sampler = api.set_sampler(self.opt, sampling_algorithm, search_size, self.data_loader)

      if category not in self.data_loader.categories:
        category = 'all'

      outputs = api.get_atomic_sequence(
        query, self.model, sampler, self.data_loader, self.text_encoder, category, print=True)

