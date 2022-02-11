
# Standard libraries
from tkinter import Label, Button, Entry, StringVar
from tkinter import W

# Other modules
from settings import *
from Viewer import Viewer

class ResearchTask(Viewer):

    maxStages = 5

    def __init__(self, root, description: str, levels: list[int], count: int=0, startRow: int=0, startCol: int=0):
        self.root = root

        self.description = description
        self.levels = levels
        self.numLevels = len(self.levels)
        self.SetStartPos(startRow, startCol)

        # User data
        self.count = count
    
    def ReadCountFromData(self, count: int):
        self.count = count
        self.CountStr.set(self.count)
        self.UpdateCompletion()
    
    def UpdateCount(self):
        self.count = int(self.CountStr.get())

        if self.count < 0:
            self.count = 0
            self.CountStr.set(0)

        self.UpdateCompletion()

    def UpdateCompletion(self):
        for i in range(self.numLevels):
            if self.count >= self.levels[i]:
                self.levelComps[i]["state"] = "disabled"
            else:
                self.levelComps[i]["state"] = "normal"

    def ViewerSetup(self):

        # Task description
        self.descriptionLabel = Label(self.root, text=self.description)

        # Task count
        self.CountStr = StringVar(self.root, value=str(self.count))
        self.countComp = Entry(self.root, textvariable=self.CountStr, width=3)

        # Task levels
        self.levelComps = [Button(self.root, text=str(level), width=3) for level in self.levels]

    def ViewerLayout(self):

        # Task description
        self.descriptionLabel.grid(row=self.startRow, column=self.startCol, sticky=W)

        # Task count
        self.countComp.grid(row=self.startRow, column=self.startCol+1)

        # Task levels
        offset = self.maxStages - self.numLevels + 2
        for index, label in enumerate(self.levelComps):
            row = self.startRow
            col = self.startCol + index + offset
            label.grid(row=row, column=col)