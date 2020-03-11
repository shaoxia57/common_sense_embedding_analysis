import os
import sys
import argparse
import torch

import dataset_creation.kb_crawl.comet.src.data.data as data
import dataset_creation.kb_crawl.comet.src.data.config as cfg
import dataset_creation.kb_crawl.comet.src.api as api

samples = 10

class CometModel:
  def __init__(self, device = 'cpu', model_file = 'dataset_creation/kb_crawl/comet/pretrained_models/conceptnet_pretrained_model.pickle', topK=10):
    self.device = device
    self.model_file = model_file
    self.sampling_algorithm = 'beam'+'-'+str(samples)
    
    self.setup()

  def setup(self):
    opt, state_dict = api.load_model_file(self.model_file)

    self.data_loader, self.text_encoder = api.load_data('conceptnet', opt)

    n_ctx = self.data_loader.max_e1 + self.data_loader.max_e2 + self.data_loader.max_r
    n_vocab = len(self.text_encoder.encoder) + n_ctx

    self.model = api.make_model(opt, n_vocab, n_ctx, state_dict)

    if self.device != 'cpu':
        cfg.device = int(self.device)
        cfg.do_gpu = True
        torch.cuda.set_device(cfg.device)
        self.model.cuda(cfg.device)
    else:
        cfg.device = 'cpu'

    # set sampler
    self.sampler = api.set_sampler(opt, self.sampling_algorithm, self.data_loader)    
    
  def query(self, query, relations):
    return api.get_conceptnet_sequence(
      query, 
      self.model, 
      self.sampler, 
      self.data_loader, 
      self.text_encoder, 
      relations
    )