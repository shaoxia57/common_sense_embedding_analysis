import os
import sys
import argparse
import torch

sys.path.append(os.getcwd())

import dataset_creation.kb_crawl.comet.src.data.data as data
import dataset_creation.kb_crawl.comet.src.data.config as cfg
import dataset_creation.kb_crawl.comet.src.api as api


if __name__ == '__main__':

    parser = argparse.ArgumentParser()
    parser.add_argument('--device', type=str, default='cpu')
    parser.add_argument('--model_file', type=str, default='models/atomic_pretrained_model.pickle')
    parser.add_argument('--sampling_algorithm', type=str, default='help')

    args = parser.parse_args()

    opt, state_dict = api.load_model_file(args.model_file)

    data_loader, text_encoder = api.load_data('atomic', opt)

    n_ctx = data_loader.max_event + data_loader.max_effect
    n_vocab = len(text_encoder.encoder) + n_ctx
    model = api.make_model(opt, n_vocab, n_ctx, state_dict)

    if args.device != 'cpu':
        cfg.device = int(args.device)
        cfg.do_gpu = True
        torch.cuda.set_device(cfg.device)
        model.cuda(cfg.device)
    else:
        cfg.device = 'cpu'

    while True:
        input_event = 'help'
        category = 'help'
        sampling_algorithm = args.sampling_algorithm

        while input_event is None or input_event.lower() == 'help':
            input_event = input('Give an event (e.g., PersonX went to the mall): ')

            if input_event == 'help':
                api.print_help(opt.dataset)

        while category.lower() == 'help':
            category = input('Give an effect type (type \'help\' for an explanation): ')

            if category == 'help':
                api.print_category_help(opt.dataset)

        while sampling_algorithm.lower() == 'help':
            sampling_algorithm = input('Give a sampling algorithm (type \'help\' for an explanation): ')

            if sampling_algorithm == 'help':
                api.print_sampling_help()

        sampler = api.set_sampler(opt, sampling_algorithm, data_loader)

        if category not in data_loader.categories:
            category = 'all'

        outputs = api.get_atomic_sequence(
            input_event, model, sampler, data_loader, text_encoder, category)

