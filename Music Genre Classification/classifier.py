import os
import pickle

import matplotlib.pyplot as plt
import numpy as np
import scipy.io.wavfile as wav
from python_speech_features import mfcc

from knn import nearest_class, get_neighbors

# Load Dataset
dataset = []


def load_dataset():
    with open("my.dat", 'rb') as f:
        while True:
            try:
                dataset.append(pickle.load(f))
            except EOFError:
                f.close()
                break


load_dataset()

# Create Result matrix
directory = "./Data/genres_original"
results = dict()
i = 1
for folder in os.listdir(directory):
    results[i] = folder
    i += 1


def classifier(path, k):
    (rate, sig) = wav.read(path)
    mfcc_feat = mfcc(sig, rate, winlen=0.020, appendEnergy=False)
    covariance = np.cov(np.matrix.transpose(mfcc_feat))
    mean_matrix = mfcc_feat.mean(0)
    feature = (mean_matrix, covariance, 0)
    predicts, votes = nearest_class(get_neighbors(dataset, feature, k))

    plt.subplot(1, 2, 1)
    plt.plot(mfcc_feat)
    plt.title("MFCC Feat")

    plt.subplot(1, 2, 2)
    plt.plot(mean_matrix)
    plt.title("Mean Matrix")

    plt.show()
    return [results[predict] for predict in predicts], votes
