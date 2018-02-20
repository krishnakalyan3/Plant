#!/usr/bin/env python3

import os
import pprint
from PIL import Image
import matplotlib.pyplot as plt
import shutil
from os.path import exists


def count_files(path):
    dir_dict = {}
    for root, dirs, files in os.walk(path):
        if len(files) > 0:
            dir_dict[root] = len(files)
    return pprint.pprint(dir_dict, width=1)


def get_stats_from_path_train(path, plot=False):
    widths = []
    heights = []

    for d in os.listdir(path):
        d = os.path.join(path, d)
        print(d)
        if os.path.isdir(d):
            for f in os.listdir(d):
                f = os.path.join(d, f)
                width, height = get_image_size(f)
                widths.append(width)
                heights.append(height)

    print('Height min: {} max: {}'.format(min(heights), max(heights)))
    print('Width min: {} max: {}'.format(min(widths), max(widths)))
    if plot:
        f, axarr = plt.subplots(1, 2)
        axarr[0].hist(widths, color='blue', label='widths')
        axarr[1].hist(heights, color='red', label='heights')

    return widths, heights


def get_stats_from_path_test(path):
    widths = []
    heights = []

    for d in os.listdir(path):
        f = os.path.join(path, d)
        width, height = get_image_size(f)
        widths.append(width)
        heights.append(height)

    #print('Height min: {} max: {}'.format(min(heights), max(heights)))
    #print('Width min: {} max: {}'.format(min(widths), max(widths)))
    return widths, heights


def get_image_size(path):
    img = Image.open(path)
    width, height = img.size
    return width, height


def create_valid(path, pct_split=.8):
    """
    path: Input Path
    pct_split: Split Percentage

    """
    val_path = path + 'valid'
    train_dir_dict = {}

    # Train dir statistics
    if not exists(val_path):
        train_path = path + 'train'
        train_master = path + 'train_master'

        for root, dirs, files in os.walk(train_path):
            if len(files) > 0:
                train_dir_dict[root] = len(files)
                print('Train Folder Name: {} Total Files: {}'.format(root, files))

        # Create a master_backup_train
        if not exists(train_master):
            shutil.copytree(train_path, train_master)

        # Compute how many files need to be copied
        for train_dir_sub in train_dir_dict:
            files_to_cp = int(train_dir_dict[train_dir_sub] * (1 - pct_split))
            # print(files_to_cp)
            train_dir_dict[train_dir_sub] = files_to_cp

            train_files = []
            # Get List of file in that direcory
            for root, dirs, files in os.walk(train_dir_sub):
                train_files = files

            # move files into valid directory
            destination = val_path + '/' + train_dir_sub.split('/')[-1]
            os.makedirs(destination)

            print('Destination Folder Name: {} Total Files: {}'.format(destination, files_to_cp))

            for i in train_files[:files_to_cp]:
                source = train_dir_sub + '/' + i
                shutil.move(source, destination + '/' + i)
    else:
        print('Validation path exists')


def metrics(y, yhat):
    from sklearn.metrics import confusion_matrix
    from sklearn.metrics import f1_score
    from sklearn.metrics import accuracy_score
    cm = confusion_matrix(y, yhat)
    f1 = f1_score(y, yhat, average='macro')
    acc = accuracy_score(y, yhat)

    # plt.matshow(cm)
    return f1, acc, cm