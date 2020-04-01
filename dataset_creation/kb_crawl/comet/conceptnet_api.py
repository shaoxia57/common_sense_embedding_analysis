import os
import sys
import argparse
import torch

import dataset_creation.kb_crawl.comet.src.data.data as data
import dataset_creation.kb_crawl.comet.src.data.config as cfg
import dataset_creation.kb_crawl.comet.src.api as api

samples = 10
pretrained_file = 'dataset_creation/kb_crawl/comet/pretrained_models/conceptnet_pretrained_model.pickle'
class CometModel:
  def __init__(self, device = 'cpu', model_file = pretrained_file):
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

        sampling_method_split = sampling_method.split('-')[0]
        sampling_algorithm = sampling_method_split[0]
        search_size = int(sampling_method.split('-')[1]) if len(sampling_method_split) > 1 else 10

      sampler = api.set_sampler(self.opt, sampling_algorithm, search_size, self.data_loader)

      if relation not in data.conceptnet_data.conceptnet_relations:
        relation = 'all'

      outputs = api.get_conceptnet_sequence(
        query, self.model, sampler, self.data_loader, self.text_encoder, relation, print=True)