from tkinter import filedialog
from tkinter import *

from Pre_Processing import *
from Classifier import *

import tkMessageBox
import os


class GUI:
    def __init__(self, win):
        print "GUI.Constructor"
        self.chosenBuilder = None
        self.trainingSet = None
        self.testSet = None
        self.Classifier = None
        self.bins = None

        self.lbl1 = Label(win, text='Directory Path')
        self.lbl2 = Label(win, text='Discretization Bins:')

        self.t1 = Entry(bd=3, width="45")
        self.t2 = Entry(width="10")

        self.btn0 = Button(win, text='Browse')
        self.btn1 = Button(win, text='Build')
        self.btn2 = Button(win, text='Classify')

        self.lbl1.place(x=30, y=50)
        self.t1.place(x=120, y=50)

        self.lbl2.place(x=10, y=100)
        self.t2.place(x=120, y=100)

        self.b0 = Button(win, text='Browse', command=self.Browse, width="10")
        self.b1 = Button(win, text='Build', command=self.Build, width="20")
        self.b2 = Button(win, text='Classify', command=self.Classify, width="20")
        self.b1.place(x=140, y=150)
        self.b2.place(x=140, y=200)
        self.b0.place(x=410, y=50)

    def Browse(self):
        # Allow user to select a directory and store it in global var
        # called folder_path
        print "GUI.Browse"
        self.t1.delete(0, 'end')
        Tk().withdraw()
        global folder_path
        filename = filedialog.askdirectory()
        folder_path.set(filename)
        self.t1.insert(0, filename)
        print "Chosen Path: " + filename

    def Build(self):
        print "GUI.Build"
        title = "Naive Bayes Classifier - Error"
        enteredPath = self.t1.get()
        if not self.ValidPath(enteredPath):
            msg = "Invalid input of path! Please check that all files are exist!"
            tkMessageBox.showinfo(title, msg)
            return
        enteredBins = self.t2.get()
        self.bins = int(enteredBins)
        if not self.ValidBins(enteredBins):
            msg = "Invalid input of bins!"
            tkMessageBox.showinfo(title, msg)
            return
        try:
            self.chosenBuilder = Pre_Processing(enteredPath, self.bins)
            self.chosenBuilder.build()
            if not self.chosenBuilder.checkValidBins(self.chosenBuilder._Data):
                msg = "You have entered invalid number of bins. Please choose another number and start again!"
                tkMessageBox.showinfo(title, msg)
                return
            else:
                self.trainingSet = self.chosenBuilder.Discretization(self.chosenBuilder._Data)
                title = "Naive Bayes Classifier"
                msg = "Building classifier using train-set is done!"
                tkMessageBox.showinfo(title, msg)
                return
        except:
            msg = "An error occurred while building the classifier!"
            tkMessageBox.showinfo(title, msg)
            return

    def Classify(self):
        print "GUI.Classify"
        if self.chosenBuilder is None:
            title = "Naive Bayes Classifier - Error"
            msg = "Please build first!"
            tkMessageBox.showinfo(title, msg)
            return
        self.testSet = self.chosenBuilder.processTestData()
        self.Classifier = Classifier(self.trainingSet, self.testSet, self.chosenBuilder.path, self.chosenBuilder._CatAttributes, self.bins)
        title = "Naive Bayes Classifier"
        msg = "Classifying process is done!"
        tkMessageBox.showinfo(title, msg)

    def ValidPath(self, user_input):
        print "GUI.ValidPath"
        if not os.path.exists(user_input) or not os.path.isdir(user_input):
            return False
        files_list = []
        files_list.append(os.path.abspath(os.path.join(user_input, 'Structure.txt')))
        files_list.append(os.path.abspath(os.path.join(user_input, 'train.csv')))
        files_list.append(os.path.abspath(os.path.join(user_input, 'test.csv')))
        for file in files_list:
            if not os.path.exists(file) or not os.path.isfile(file) or not os.path.getsize(file) > 0:
                return False
        return True

    def ValidBins(self, user_input):
        print "GUI.validBins"
        try:
            # input is not empty
            if user_input == '':
                return False
            # input is int value
            val = int(user_input)
            if val < 1:
                return False
            return True
        except ValueError:
            return False


window = Tk()
folder_path = StringVar()
classifierWindow = GUI(window)
window.title('Naive Bayes Classifier')
window.geometry("500x300")
window.mainloop()
