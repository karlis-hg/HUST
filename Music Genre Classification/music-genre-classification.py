import os
import pickle
import random

import numpy as np
import scipy.io.wavfile as wav
from python_speech_features import mfcc

from knn import nearest_class, get_neighbors, get_accuracy


directory = "./Data/genres_original"
f = open("my.dat", 'wb')
i = 0

for folder in os.listdir(directory):
    i += 1
    if i == 11:
        break
    for file in os.listdir(directory+"/"+folder):
        # Get Sample rate and data of audio
        (rate, sig) = wav.read(directory+"/"+folder+"/"+file)
        # Extract MFCC from audio data
        mfcc_feat = mfcc(sig, rate, winlen=0.020, appendEnergy=False)
        # Calculate the covariance (how related are the two mfcc)
        covariance = np.cov(np.matrix.transpose(mfcc_feat))
        # Calculate the mean of MFCC (the central tendency of the MFCC)
        mean_matrix = mfcc_feat.mean(0)
        # Create a tuple containing the mean matrix, covariance and a class label
        feature = (mean_matrix, covariance, i)
        # Record the tuple in file
        pickle.dump(feature, f)

f.close()

dataset = []


def load_dataset(split, trSet, teSet):
    with open("my.dat", 'rb') as f1:
        while True:
            try:
                dataset.append(pickle.load(f1))
            except EOFError:
                f1.close()
                break

    for x in range(len(dataset)):
        if random.random() < split:
            trSet.append(dataset[x])
        else:
            teSet.append(dataset[x])


training_set = []
test_set = []
load_dataset(0.66, training_set, test_set)

predictions = []
for y in range(len(test_set)):
    predicts, votes = nearest_class(get_neighbors(dataset, test_set[y], 7))
    predictions.append(predicts[0])

accuracy = get_accuracy(test_set, predictions) * 100
print(f"The accuracy is about{accuracy: .2f}%")
