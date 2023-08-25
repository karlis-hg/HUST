import operator
import numpy as np


def distance_cal(instance1, instance2, k):
    mm1 = instance1[0]
    cm1 = instance1[1]
    mm2 = instance2[0]
    cm2 = instance2[1]
    distance = np.trace(np.dot(np.linalg.inv(cm2), cm1))
    distance += (np.dot(np.dot((mm2 - mm1).transpose(), np.linalg.inv(cm2)), mm2 - mm1))
    distance += np.log(np.linalg.det(cm2)) - np.log(np.linalg.det(cm1))
    distance -= k
    return distance


def get_neighbors(trainingSet, instance, k):
    distances = []
    for x in range(len(trainingSet)):
        dist = distance_cal(trainingSet[x], instance, k) + distance_cal(instance, trainingSet[x], k)
        distances.append((trainingSet[x][2], dist))
    distances.sort(key=operator.itemgetter(1))
    neighbors = []
    for x in range(k):
        neighbors.append(distances[x][0])
    return neighbors


def nearest_class(neighbors):
    class_vote = {}
    for x in range(len(neighbors)):
        response = neighbors[x]
        if response in class_vote:
            class_vote[response] += 1
        else:
            class_vote[response] = 1
    sorter = sorted(class_vote.items(), key=operator.itemgetter(1), reverse=True)
    genres = []
    votes = []
    for item in sorter:
        genres.append(item[0])
        votes.append(item[1])
    return genres, votes


def get_accuracy(testSet, predictions):
    correct = 0
    for x in range(len(testSet)):
        if testSet[x][-1] == predictions[x]:
            correct += 1
    return 1.0*correct/len(testSet)
