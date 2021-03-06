import os

import torch
import numpy as np
from PIL import Image

import logging
logging.basicConfig(level = logging.INFO, handlers = [logging.StreamHandler()],
                    format = "%(asctime)s — %(name)s — %(levelname)s — %(message)s")


def load_img(img_path):
    """
    both read fname image and resize it

    :param:
        img_path : str, path to the image file
    """
    assert os.path.isfile(img_path), f'img file not exist: {img_path}'
    img = Image.open(img_path)
    return img.convert('RGB')


def save_img(w_path, data):
    """
    :param:
        w_path : str, path to write the image
        data : Tensors, (C, H, W)
    """
    img = data.clone().clamp(0, 255).cpu().numpy()
    img = img.transpose(1, 2, 0).astype(np.uint8)
    img = Image.fromarray(img)
    img.save(w_path)
    logging.info(f'image written: {w_path}')
    return None


def process_img(img_path, tfms):
    """
    load in image and transform it into Tensors, ready for model input
    """
    assert os.path.isfile(img_path), f'img_path not exist: {img_path}'
    content_img = load_img(img_path)    
    content_img = tfms(content_img)
    # convert to (B, C, H, W)
    content_img = content_img.unsqueeze(0)
    return content_img