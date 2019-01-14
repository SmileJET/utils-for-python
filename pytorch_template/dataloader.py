# encoding:utf8

import os

import cv2
import numpy as np
from torch.utils import data
from PIL import Image


class data_loader(data.Dataset):
    def __init__(self, args, train=True):
        self.args = args
        self._root = os.path.join(args.root_path, args.img_path)

        if train:
            npy = np.load(os.path.join(args.npy_path, args.type_train_npy))
        else:
            npy = np.load(os.path.join(args.npy_path, args.type_test_npy))

        self._img_list = npy[:, 0]
        self._label = np.array([int(label)-1 for label in npy[:, 1]])
        self.PIXEL_MEANS = np.array([50])
        self.WINDOWING = [-1024, 3071]

    def __getitem__(self, idx):
        if isinstance(self._img_list[0], bytes):
            img_path = os.path.join(self._root, bytes.decode(self._img_list[idx]))
        else:
            img_path = os.path.join(self._root, self._img_list[idx])
        label = self._label[idx]
        img = cv2.imread(img_path, -1)
        img = img.astype(np.float32, copy=False)-32768
        img = cv2.resize(img, (self.args.image_size, self.args.image_size), interpolation=cv2.INTER_LINEAR)
        img = self.windowing(img, self.WINDOWING)
        img -= self.PIXEL_MEANS
        im_tensor = self.im_list_to_blob(img)

        im_tensor/=255.0

        return im_tensor, label

    def __len__(self):
        return len(self._img_list)

    def im_list_to_blob(self, im, use_max_size=False):
        """Convert a list of images into a network input.
        """
        # max_shape = np.array([im.shape for im in ims]).max(axis=0)
        # min_shape = np.array([im.shape for im in ims]).min(axis=0)
        # print max_shape, min_shape
        if use_max_size:
            # max_shape = np.array([config.MAX_SIZE, config.MAX_SIZE])
            max_shape = np.array([512, 512])
        else:
            max_shape = np.array([im.shape]).max(axis=0)
        # num_channel = ims[0].shape[2] if ims[0].ndim == 3 else 3
        num_channel = 1
        blob = np.zeros((num_channel, max_shape[0], max_shape[1]),
                        dtype=np.float32)

        if im.ndim == 2:
            for chn in range(num_channel):
                blob[chn, :im.shape[0], :im.shape[1]] = im
        elif im.ndim == 3:
            blob[:, :im.shape[0], :im.shape[1]] = im.transpose((2, 0, 1))

        return blob

    def windowing(self, im, win):
        # scale intensity from win[0]~win[1] to float numbers in 0~255
        im1 = im.astype(float)
        im1 -= win[0]
        im1 /= win[1] - win[0]
        im1[im1 > 1] = 1
        im1[im1 < 0] = 0
        im1 *= 255
        return im1