import os
import pandas as pd


class Pre_Processing:
    def __init__(self, user_path, bins):
        print "Pre_Processing.Constructor"
        self._m_estimator = 2
        self._Structure = {}
        self._NumericAttributes = {}
        self._CatAttributes = {}
        self._Data = []
        self._Bins = bins
        self.path = user_path

    def readStructure(self):
        print "Pre_Processing.readStructure"
        _path = os.path.abspath(os.path.join(self.path, "Structure.txt"))
        if os.path.isfile(_path):
            # _path = os.path.abspath(os.path.join( _mainPath , "Structure.txt"))
            _file = open(_path, 'rb')
            _lines = _file.readlines()
            for i in range(len(_lines)):
                _currentLine = _lines[i].replace("\r\n", '')
                _splittedLine = _currentLine.split(" ")
                # Check if the attribute is numeric or categorial attribute
                if _splittedLine[2].find("{") != -1:  # The attribute is categorial
                    _categories = self.splitCategorial(_currentLine)
                    self._CatAttributes[_splittedLine[1]] = _categories
                else:  # The attribute is numeric
                    self._NumericAttributes[_splittedLine[1]] = None
            return True
        else:
            return False

    def splitCategorial(self, _currentLine):
        print "Pre_Processing.splitCategorial"
        _splittedLine = _currentLine.split("{")
        _categoriesLine = _splittedLine[1].replace("}", '')
        return _categoriesLine

    def readTrain(self):
        print "Pre_Processing.readTrain"
        fileAbsPath = os.path.abspath(os.path.join(self.path, "train.csv"))
        self._Data = pd.read_csv(fileAbsPath)
        for x in self._Data:
            if x in self._NumericAttributes.keys():
                self._Data[x].fillna((self._Data[x].mean()), inplace=True)
            elif x in self._CatAttributes.keys():
                self._Data[x].fillna(self._Data[x].mode()[0], inplace=True)

    def readTest(self, set):
        for x in set:
            if x in self._NumericAttributes.keys():
                set[x].fillna((set[x].mean()), inplace=True)
            elif x in self._CatAttributes.keys():
                set[x].fillna(set[x].mode()[0], inplace=True)
        return set

    def Discretization(self, set):
        # Define min and max values:
        print "Pre_Processing.Discretization"
        if self.checkValidBins(set) == False:
            return None
        for x in self._NumericAttributes.keys():
            labels = range(self._Bins)
            # Binning using cut function of pandas
            set[x] = pd.cut(set[x], bins=self._Bins, labels=labels, include_lowest=True)
        return set

    def processTestData(self):
        print "Pre_Processing.processTestData"
        data = pd.read_csv(os.path.abspath(os.path.join(self.path, "test.csv")))
        data = self.readTest(data)
        return self.Discretization(data)

    def checkValidBins(self, set):
        print "Pre_Processing.checkValidBins"
        for x in self._NumericAttributes:
            minval = set[x].min()
            maxval = set[x].max()
            #if (self._Bins > maxval - minval):
            #    return False
            # print ("column:", x, "bin size:",(maxval - minval) /self._Bins )
        return True

    def build(self):
        self.readStructure()
        self.readTrain()
