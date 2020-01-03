# script meant to extract features from curated training data and put features into an input vector for ANN as well as create
# a target vector for labels

import os
import sys

import MusEEG
from MusEEG import eegData
import pandas as pandas
import numpy as np


def createTargetVector(objarray, *argv):
    labels = []
    targets = [0 for row in range(len(objarray[0][:]) * len(objarray))]
    index = 0
    for i in range(0, len(objarray)):
        print(objarray[i][0].filename)
        for j in range(0, len(objarray[i])):
            labels.append(objarray[i][j].filename)
            for arg in argv:
                if arg in objarray[i][j].filename:
                    targets[index] = i
                    index = index + 1
    return targets

numofSamples = 77

# create object lists, for easier handling
smile = [eegData() for i in range(0, numofSamples)]
# biteLowerLip = [eegData() for i in range(0, numofSamples)]
eyebrows = [eegData() for i in range(0, numofSamples)]
hardBlink = [eegData() for i in range(0, numofSamples)]
lookLeft = [eegData() for i in range(0, numofSamples)]
lookRight = [eegData() for i in range(0, numofSamples)]
neutral = [eegData() for i in range(0, numofSamples)]
scrunch = [eegData() for i in range(0, numofSamples)]
# tongue = [eegData() for i in range(0, numofSamples)]

# load chunks for each of the objects, 60 from trainbatch1 and 60 from trainbatch2
for i in range(0, numofSamples):
    neutral[i].loadChunkFromTraining(subdir=os.path.join('trainbatch2_improved_320samples', 'bigChunks'),
                                     filename='neutral_' + str(i) + '.csv', labelcols=False)

for i in range(0, numofSamples):
    smile[i].loadChunkFromTraining(subdir=os.path.join('trainbatch2_improved_320samples', 'bigChunks'),
                                   filename='smile_' + str(i) + '.csv', labelcols=False)
    # biteLowerLip[i].loadChunkFromTraining(subdir=os.path.join('trainbatch1', 'bigChunks'),
    #                                       filename='bitelowerlip_' + str(i) + '.csv', labelcols=False)
    eyebrows[i].loadChunkFromTraining(subdir=os.path.join('trainbatch2_improved_320samples', 'bigChunks'),
                                      filename='eyebrows_' + str(i) + '.csv', labelcols=False)
    lookLeft[i].loadChunkFromTraining(subdir=os.path.join('trainbatch2_improved_320samples', 'bigChunks'),
                                      filename='lookleft_' + str(i) + '.csv', labelcols=False)
    lookRight[i].loadChunkFromTraining(subdir=os.path.join('trainbatch2_improved_320samples', 'bigChunks'),
                                       filename='lookright_' + str(i) + '.csv', labelcols=False)
    scrunch[i].loadChunkFromTraining(subdir=os.path.join('trainbatch2_improved_320samples', 'bigChunks'),
                                     filename='scrunch_' + str(i) + '.csv', labelcols=False)
    # tongue[i].loadChunkFromTraining(subdir=os.path.join('trainbatch2_improved_320samples', 'bigChunks'),
    #                                 filename='tongue_' + str(i) + '.csv', labelcols=False)
    hardBlink[i].loadChunkFromTraining(subdir=os.path.join('trainbatch2_improved_320samples', 'bigChunks'),
                                       filename='hardblink_' + str(i) + '.csv', labelcols=False)

# for i in range(60, numofSamples):
#     smile[i].loadChunkFromTraining(subdir=os.path.join('trainbatch2', 'bigChunks'),
#                                    filename='smile_' + str(i-60) + '.csv')
#     # biteLowerLip[i].loadChunkFromTraining(subdir=os.path.join('trainbatch2', 'bigChunks'),
#     #                                       filename='bitelowerlip_' + str(i-60) + '.csv')
#     eyebrows[i].loadChunkFromTraining(subdir=os.path.join('trainbatch2', 'bigChunks'),
#                                       filename='eyebrows_' + str(i-60) + '.csv')
#     lookLeft[i].loadChunkFromTraining(subdir=os.path.join('trainbatch2', 'bigChunks'),
#                                       filename='lookleft_' + str(i-60) + '.csv')
#     lookRight[i].loadChunkFromTraining(subdir=os.path.join('trainbatch2', 'bigChunks'),
#                                        filename='lookright_' + str(i-60) + '.csv')
#     scrunch[i].loadChunkFromTraining(subdir=os.path.join('trainbatch2', 'bigChunks'),
#                                      filename='scrunch_' + str(i-60) + '.csv')
#     # tongue[i].loadChunkFromTraining(subdir=os.path.join('trainbatch2', 'bigChunks'),
#     #                                 filename='tongue_' + str(i-60) + '.csv')
#     hardBlink[i].loadChunkFromTraining(subdir=os.path.join('trainbatch2', 'bigChunks'),
#                                        filename='hardblink_' + str(i-60) + '.csv')

# create single list with all of other gesture lists.
# gestures = [smile, biteLowerLip, eyebrows, hardBlink, lookLeft, lookRight, neutral, scrunch]

gestures = [smile, eyebrows, hardBlink, lookLeft, lookRight, neutral, scrunch]
# targets = createTargetVector(gestures, 'smile', 'bitelowerlip', 'eyebrows', 'hardblink', 'lookleft', 'lookright',
#                              'neutral', 'scrunch')
targets = createTargetVector(gestures, 'smile', 'eyebrows', 'hardblink', 'lookleft', 'lookright',
                             'neutral', 'scrunch')


inputs = np.ndarray([len(gestures)*numofSamples, 350])
inputindex = 0
for i in range(0, len(gestures)):
    for j in range(0, len(gestures[0])):
        print(j)
        gestures[i][j].wavelet()
        gestures[i][j].extractStatsFromWavelets()
        gestures[i][j].flattenIntoVector()
        inputs[inputindex][:] = gestures[i][j].inputVector
        inputindex = inputindex + 1

print(targets)

inputs = pandas.DataFrame(inputs)
targets = pandas.DataFrame(targets)

inputs.to_csv(os.path.join(MusEEG.parentDir, 'data', 'training', 'batch2_improved_320samples', 'bigChunks', 'inputs.csv'))
targets.to_csv(os.path.join(MusEEG.parentDir, 'data', 'training', 'batch2_improved_320samples', 'bigChunks', 'targets.csv'))