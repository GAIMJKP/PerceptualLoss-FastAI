import os

import torch
import torch.nn as nn

from src.model.hook import VGGHooks
from src.model.vgg import VGG16
from src.model.transformer_net import TransformerNet

import logging
logging.basicConfig(level = logging.INFO, handlers = [logging.StreamHandler()],
                    format = "%(asctime)s — %(name)s — %(levelname)s — %(message)s")


class MetaModel(nn.Module):
    """
    meta model subclass to glue transfomrer net + vgg
    also attach hooks in the subclass and return it in self.forward()
    """
    IMAGENET_MEAN = [0.485, 0.456, 0.406]
    IMAGENET_STD = [0.229, 0.224, 0.225]

    def __init__(self, vgg_grad = False):
        super(MetaModel, self).__init__()
        self.vgg = VGG16(requires_grad = vgg_grad)
        self.transformer = TransformerNet()
        
        device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
        self.mean = torch.tensor(self.IMAGENET_MEAN).view(-1, 1, 1).to(device)
        self.std = torch.tensor(self.IMAGENET_STD).view(-1, 1, 1).to(device)

        logging.info('meta model is set')

    def normalize_batch(self, x):
        """ x -- Tensors, (B, C, H, W) """
        x = x.div_(255.)
        return (x - self.mean) / self.std

    def forward(self, x, vgg_only = False):
        out = x if vgg_only else self.transformer(x)
        out = self.vgg(self.normalize_batch(out))
        return out
