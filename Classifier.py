import os
import pandas as pd


class Classifier:
    def __init__(self, trainSet, testSet, mainPath, categorialAtt, bins):
        print "Classifier.Constructor"
        self._TrainSet = trainSet
        self._TestSet = testSet
        self._MainPath = mainPath
        self.bins = bins
        self.categorialAtt = categorialAtt
        self._m = 2.0
        # self._TestSet = self.readTestSet()
        self._Attributes = self.getAttributesValues()
        self._Probabilities = {}
        self.calcProbabilities()
        self.classify()

    # def readTestSet(self):
    #     fileAbsPath = os.path.abspath(os.path.join(self._MainPath, "test.csv"))
    #     return pd.read_csv(fileAbsPath)

    def is_number(self, n):
        try:
            float(n)
        except ValueError:
            return False
        return True

    def getAttributesValues(self):
        _attributes = {}
        for x in self._TrainSet:
            # _attributes[x] = [self._TrainSet[x], len(set(self._TrainSet[x]))]
            if x in self.categorialAtt.keys():
                elements = self.categorialAtt[x].split(',')
                attSet = {}
                for elem in elements:
                    if self.is_number(elem):
                        attSet[elem] = (float(elem))
                    else:
                        attSet[elem] = elem
                _attributes[x] = [set(attSet.values()), len(set(self._TrainSet[x]))]
                # _attributes[x] = [set(self.categorialAtt[x].split(',')), len(set(self._TrainSet[x]))]
            else:
                _attributes[x] = [set(range(0, self.bins)), len(set(self._TrainSet[x]))]
            # _uniqueValues = set(self._TrainSet[x])
            # _attributes[x] = [_uniqueValues, len(_uniqueValues)]
        return _attributes

    def calcProbabilities(self):
        differentClass = self._Attributes['class'][0]
        for x in self._Attributes:
            if not x == 'class':
                self._Probabilities[x] = {}
                for z in self._Attributes[x][0]:
                    self._Probabilities[x][z] = {}
                    for y in differentClass:
                        _NC = len(self._TrainSet.loc[(self._TrainSet[x] == z) & (self._TrainSet['class'] == y)])
                        _n = len(self._TrainSet.loc[self._TrainSet['class'] == y])
                        _p = 1.0 / self._Attributes[x][1]
                        # if _p == 0 or _n == 0 or _NC == 0:
                        #     print "------"
                        self._Probabilities[x][z][y] = (_NC + self._m * _p) / (_n + self._m)

    def classify(self):
        print "Classifier.classify"
        differentClass = self._Attributes['class'][0]
        writeToFile = ''
        for row in range(0, len(self._TestSet['class'])):
            results = {}
            for resClass in differentClass:
                prob = 1.0
                for attribute in self._Attributes:
                    if attribute != 'class':
                        value = self._TestSet[attribute][row]
                        prob *= self._Probabilities[attribute][value][resClass]
                results[resClass] = prob
            classified = max(results, key=results.get)
            if classified == 'Y':
                res = 'yes'
            else:
                res = 'no'
            writeToFile += str(row + 1) + " " + res + '\n'
        with open(os.path.abspath(os.path.join(self._MainPath, 'output.txt')), 'w') as outPutFile:
            outPutFile.write(writeToFile)
