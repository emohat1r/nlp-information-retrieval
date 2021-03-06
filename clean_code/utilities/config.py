import os
import torch

from utilities.nltk_helpers import stop


class Config():
    def __init__(self, remove_nonbinary=True, include_captions=False, augment_binary=True, cosine_similarity=True,
                 image_layer='None', projection='CBOW', sequential=False, concat=False,
                 batch_size=256, test_batch_size=32, complexity='easy', learning_rate=0.00001):
        self.DEBUG = False
        self.CUDA = torch.cuda.is_available()
        self.stem = False
        self.captions_batch_size = batch_size
        self.questions_batch_size = batch_size
        self.val_batch_size = test_batch_size
        self.test_batch_size = test_batch_size
        self.stopwords = False
        self.stop = None

        torch.manual_seed(42)

        self.learning_rate = learning_rate

        self.img_data = 'data/img_data'
        self.text_data = 'data/text_data'
        self.complexity = complexity
        self.image_layer = image_layer
        self.image_layer_str = 'simple' if self.image_layer == 'None' else self.image_layer
        self.remove_nonbinary = remove_nonbinary
        self.remove_nonbinary_str = 'bin' if self.remove_nonbinary else 'all'
        self.augment_binary = augment_binary
        self.augment_binary_str = 'aug' if self.augment_binary else 'non_aug'
        self.include_captions = include_captions
        self.include_captions_str = 'cap' if self.include_captions else 'no_cap'

        self.cosine_similarity = cosine_similarity
        self.cosine_similarity_str = 'cosine' if self.cosine_similarity else 'euclidean'

        self.sequential = sequential
        self.sequential_str = 'sequential' if sequential else 'individual'

        self.concat = concat
        self.concat_str = 'concat' if concat else 'individual'

        self.projection = projection
        self.projection_str = self.projection
        self.stem_str = 'stem' if self.stem else 'no_stem'
        self.stop_str = 'stop' if self.stopwords else 'no_stop'

        self.uid_str = str.format('{}_{}_{}_{}_{}_{}_{}_{}_{}_{}', self.complexity, self.sequential_str, self.concat_str, self.projection_str,
                                  self.remove_nonbinary_str, self.augment_binary_str, self.include_captions_str,
                                  self.cosine_similarity_str, self.image_layer_str, str(batch_size))
        self.pickle_uid_str = str.format('{}_{}_{}_{}_{}_{}', self.stem_str, self.stop_str, self.remove_nonbinary_str, self.augment_binary_str,
                                         self.include_captions_str, self.concat_str)

        self.save_path_latest = str.format('data/{}/checkpoint_latest.pth.tar', self.uid_str)
        self.save_path_best = str.format('data/{}/checkpoint_best.pth.tar', self.uid_str)

        self.img_feat_file = os.path.join(self.img_data, 'IR_image_features.h5')
        self.img_map_file = os.path.join(self.img_data, 'IR_img_features2id.json')

        self.json_train_file = os.path.join(self.text_data,
                                            '{}/IR_train_{}.json'.format(self.complexity.capitalize(), self.complexity))
        self.json_val_file = os.path.join(self.text_data,
                                          '{}/IR_val_{}.json'.format(self.complexity.capitalize(), self.complexity))
        self.json_test_file = os.path.join(self.text_data,
                                           '{}/IR_test_{}.json'.format(self.complexity.capitalize(), self.complexity))

        self.pickle_captions_train_file = os.path.join(self.text_data,
                                                       '{}/IR_train_captions_{}.pkl'.format(
                                                           self.complexity.capitalize(),
                                                           self.pickle_uid_str))
        self.pickle_questions_train_file = os.path.join(self.text_data,
                                                        '{}/IR_train_questions_{}.pkl'.format(
                                                            self.complexity.capitalize(), self.pickle_uid_str))
        self.pickle_val_file = os.path.join(self.text_data,
                                            '{}/IR_val_{}.pkl'.format(self.complexity.capitalize(),
                                                                      self.pickle_uid_str))
        self.pickle_test_file = os.path.join(self.text_data,
                                             '{}/IR_test_{}.pkl'.format(self.complexity.capitalize(),
                                                                        self.pickle_uid_str))

        self.pickle_vocab_file = os.path.join(self.text_data,
                                              '{}/vocab_{}.pkl'.format(self.complexity.capitalize(),
                                                                       self.pickle_uid_str))

        self.pickle_questions_histograms_file = os.path.join(self.text_data,
                                                             '{}/histogram_questions_{}.pkl'.format(
                                                                 self.complexity.capitalize(),
                                                                 self.pickle_uid_str))
        self.pickle_captions_histograms_file = os.path.join(self.text_data,
                                                            '{}/histogram_captions_{}.pkl'.format(
                                                                self.complexity.capitalize(),
                                                                self.pickle_uid_str))
        self.pickle_val_histograms_file = os.path.join(self.text_data,
                                                       '{}/histogram_val_{}.pkl'.format(
                                                           self.complexity.capitalize(),
                                                           self.pickle_uid_str))
        self.pickle_test_histograms_file = os.path.join(self.text_data,
                                                        '{}/histogram_test_{}.pkl'.format(
                                                            self.complexity.capitalize(),
                                                            self.pickle_uid_str))

        # if not os.path.exists(self.uid_str):
        #     os.mkdir(self.uid_str)
        if not os.path.exists('data/' + self.uid_str):
            os.mkdir('data/' + self.uid_str)
