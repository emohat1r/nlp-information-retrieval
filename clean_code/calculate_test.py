from collections import defaultdict
import torch.optim as optim

from datasets.dataloaders import DataLoaderFactory
from model.cbow import CBOW
from model.rnn1 import RNN1
from model.checkpointer import save_checkpoint
from model.train import train
from model.test import test
from utilities.config import Config
import numpy as np
import torch
import time
import pickle
from model.image_layers import MLP1, MLP2
from utilities.data_helpers import plot_histogram

from utilities.helper_functions import str2bool

"""Application entry point."""
import argparse


def main():
    """Main entry point of application."""
    parser = argparse.ArgumentParser(
        description='Parser for training parameters.'
    )
    parser.add_argument(
        '--onlybin',
        help='Exclude non-binary questions',
        type=str,
        default='True'
    )
    parser.add_argument(
        '--captions',
        help='Include captions.',
        type=str,
        default='False'
    )
    parser.add_argument(
        '--augment',
        help='Augment binary questions',
        type=str,
        default='True'
    )
    parser.add_argument(
        '--epochs',
        help='Number of epochs',
        type=int,
        default=50
    )
    parser.add_argument(
        '--cosine',
        help='Whether to use cosine similarity or euclidean distance',
        type=str,
        default='True'
    )
    parser.add_argument(
        '--image_layer',
        help='which image layer to use',
        type=str,
        default='None'
    )
    parser.add_argument(
        '--projection',
        help='whether use CBOW or RNN for word concatenation',
        type=str,
        default='CBOW'
    )
    parser.add_argument(
        '--sequential',
        help='use CBOW or RNN for word concatenation',
        type=str,
        default='False'
    )
    parser.add_argument(
        '--concat',
        help='whether to consider all text as one',
        type=str,
        default='False'
    )
    parser.add_argument(
        '--batch_size',
        help='batch size',
        type=int,
        default=64
    )
    parser.add_argument(
        '--test_batch_size',
        help='test_batch size',
        type=int,
        default=32
    )
    parser.add_argument(
        '--lr',
        help='learning rate',
        type=float,
        default=0.0001
    )
    parser.add_argument(
        '--target_space',
        help='dimensionality of target space',
        type=float,
        default=True
    )
    parser.add_argument(
        '--complexity',
        help='choose between easy and hard dataset',
        type=str,
        default='easy'
    )



    args = parser.parse_args()
    onlybin = str2bool(args.onlybin)
    captions = str2bool(args.captions)
    augment = str2bool(args.augment)
    epochs = args.epochs
    image_layer = args.image_layer
    cosine_similarity = str2bool(args.cosine)
    projection = args.projection
    sequential = str2bool(args.sequential)
    concat = str2bool(args.concat)
    batch_size = int(args.batch_size)
    test_batch_size = int(args.test_batch_size)
    complexity = args.complexity
    learning_rate = float(args.lr)

    config = Config(include_captions=captions, remove_nonbinary=onlybin, augment_binary=augment,
                    cosine_similarity=cosine_similarity, image_layer=image_layer, projection=projection,
                    sequential=sequential, concat=concat, batch_size=batch_size, test_batch_size=test_batch_size,
                    complexity=complexity, learning_rate=learning_rate)

    factory = DataLoaderFactory(config)

    w2i = defaultdict(lambda: len(w2i))
    UNK = w2i["<unk>"]
    best_top1 = 0.0

    # captions_dataset, captions_dataloader = factory.generate_captions_dataset(w2i)
    questions_dataset, questions_dataloader = factory.generate_questions_dataset(w2i)

    # print(questions_dataset.sentences_histograms)
    # plot_histogram(questions_dataset.sentences_histograms)
    # print(captions_dataset.sentences_histograms)
    # plot_histogram(captions_dataset.sentences_histograms)

    w2i = defaultdict(lambda: UNK, questions_dataset.vocab)

    # val_dataset, val_dataloader = factory.generate_val_dataset(w2i)
    test_dataset, test_dataloader = factory.generate_test_dataset(w2i)

    model_best = torch.load(config.save_path_best)
    test_loss, test_loss_avg, top1, top3, top5 = test(model_best['model'], image_layer, val_dataloader, config)
    print(test_loss, test_loss_avg, top1, top3, top5)
    pickle.dump([test_loss, test_loss_avg, top1, top3, top5], open(str.format('data/{}/plot_list_test.pkl', config.uid_str), 'wb'))
    # for root, dirs, files in os.walk('../plots/'):
    #     if 'plot_list.pkl' in files:
    #         print(root)
    #         path = os.path.join(root, 'plot_list.pkl')
    #         model_latest = torch.load(os.path.join(root, 'checkpoint_best.pth.tar'))
    #         test_loss, test_loss_avg, top1, top3, top5 = test(model_latest['model'], image_layer, val_dataloader, config)
    #         print(test_loss, test_loss_avg, top1, top3, top5)
    #
    # import matplotlib.pyplot as plt
    # plt.plot(losses)
    # plt.show()


if __name__ == '__main__':
    main()
