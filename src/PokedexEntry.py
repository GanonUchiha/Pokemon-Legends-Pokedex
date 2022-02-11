import tkinter as tk
import json

from settings import *
from Viewer import Viewer
from ResearchTaskManager import ResearchTaskManager

class PokedexEntry(Viewer):

    debug = False

    def __init__(self, number: str, root=None, startRow: int=0, startCol: int=0):
        if root == None:
            self.root = tk.Tk()
        else:
            self.root = root

        self.number = number

        self.SetStartPos(startRow, startCol)
        self.PokedexSetup()
        self.ViewerSetup()
        self.ViewerLayout()

    def ExitViewer(self):
        self.root.quit()

    def PokedexSetup(self):
        self.pokedexFilename = "{:03}.json".format(self.number)
        self.pokedexFilePath = POKEDEX_DIR.joinpath(self.pokedexFilename)

        if self.pokedexFilePath.exists():
            self.data = json.load(self.pokedexFilePath.open(encoding="utf-8"))
        
        if self.debug:
            print(self.data)

        self.name = self.data[PKMN_NAME]
        self.category = self.data[PKMN_CATEGORY]
        self.type = self.data[PKMN_TYPE]
        self.food = self.data[PKMN_FOOD]
        self.holdItem = self.data[PKMN_HOLDITEM]
        self.taskManager = ResearchTaskManager(self.root, self.number)

    def ViewerSetup(self):
        # Basic info
        self.numberLabel        = tk.Label(self.root, text="No. {number}".format(number=self.number))
        self.nameLabel          = tk.Label(self.root, text=self.name)
        self.categoryLabel      = tk.Label(self.root, text="{category}神奇寶貝".format(category=self.category))
        self.typeTitleLabel     = tk.Label(self.root, text="屬性")
        self.typeComp1          = tk.Button(self.root, text=self.type[0], width=8)
        if len(self.type) > 1:
            self.typeComp2      = tk.Button(self.root, text=self.type[1], width=8)
        self.holdItemTitleLabel = tk.Label(self.root, text="持有物")
        self.holdItemLabel      = tk.Label(self.root, text="、".join(self.holdItem))

        # Food
        self.foodTitleLabel     = tk.Label(self.root, text="愛吃的食物")
        self.foodComps = list[tk.Button]()
        for foodType in PKMN_FOOD_TYPES:  # type: str
            compState = "disabled"
            if foodType in self.food:
                compState = "normal"
            component           = tk.Button(self.root, text=foodType, state=compState, width=3)
            self.foodComps.append(component)

        # Research tasks
        ## TODO: Setup for ResearchTaskManager
        self.taskManager.ViewerSetup()

    
    def ViewerLayout(self):

        root = self.root
        while not type(root) is tk.Tk:
            print(type(root))
            root = root.master
        root.title("No. {number} {name}".format(number=self.number, name=self.name))

        # Basic info
        self.numberLabel        .grid(row=0, column=0, sticky=tk.E)
        self.nameLabel          .grid(row=0, column=1, columnspan=2)
        self.categoryLabel      .grid(row=0, column=3, columnspan=len(PKMN_FOOD_TYPES)-2)

        self.typeTitleLabel     .grid(row=1, column=0, sticky=tk.W)
        self.typeComp1          .grid(row=1, column=1, columnspan=2, sticky=tk.W)
        if len(self.type) > 1:
            self.typeComp2      .grid(row=1, column=3, columnspan=2, sticky=tk.W)

        self.foodTitleLabel     .grid(row=2, column=0, sticky=tk.W)
        for index, comp in enumerate(self.foodComps):
            comp.grid(row=2, column=1+index, sticky=tk.W)

        self.holdItemTitleLabel .grid(row=3, column=0, sticky=tk.W)
        self.holdItemLabel      .grid(row=3, column=1, columnspan=len(PKMN_FOOD_TYPES)-1, sticky=tk.W)

        # Research tasks
        ## TODO: Setup layout for ResearchTaskManager
        self.taskManager.SetStartPos(0, 2 + len(PKMN_FOOD_TYPES) + 1)
        # self.taskManager.SetStartPos(4, 0)
        self.taskManager.ViewerLayout()

    def RunWindow(self):
        self.root.mainloop()