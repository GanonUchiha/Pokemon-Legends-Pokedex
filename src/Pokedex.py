
# Standard Libraries
from tkinter import Tk, PanedWindow, Button, Label
from tkinter import NSEW
from tkinter import font

# Other modules
from settings import *
from Viewer import Viewer
from PokedexEntry import PokedexEntry
from ResearchTaskManager import ResearchTaskManager

class Pokedex(Viewer):

    debug = False
    prevPageText = "上一頁 No. {number}" # type: str
    nextPageText = "下一頁 No. {number}" # type: str

    def __init__(self, root=None):
        if root == None:
            root = Tk()
        
        self.root = root

        self.GetAllPages()
        self.DefaultConfig()
        self.ViewerSetup()
        self.ViewerLayout()
        self.Centering()
        # self.GridConfig()
    
    def GetAllPages(self):
        self.pages = list[int]()
        for file in POKEDEX_DIR.glob("*.json"):
            if self.debug:
                print(file.stem)
            try:
                self.pages.append(int(file.stem))
            except:
                pass
        print(self.pages)

        self.currentPageIndex = 0
    
    def UpdatePageButtons(self):
        self.prevPageIndex = (self.currentPageIndex + len(self.pages) - 1) % len(self.pages)
        self.nextPageIndex = (self.currentPageIndex + 1) % len(self.pages)
        
        self.prevButton.configure(text=self.prevPageText.format(number=self.pages[self.prevPageIndex]))
        self.nextButton.configure(text=self.nextPageText.format(number=self.pages[self.nextPageIndex]))

        # Pokedex Pane
        self.pokedexPanel.grid_forget()
        self.pokedexPanel = PanedWindow(self.root)
        self.pokedexEntry = PokedexEntry(self.pages[self.currentPageIndex], self.pokedexPanel)
        self.pokedexPanel.grid(row=1, column=2)

        # Research Task Pane
        self.taskPanel.grid_forget()
        self.taskPanel = PanedWindow(self.root)
        self.taskEntry = ResearchTaskManager(self.taskPanel, self.pages[self.currentPageIndex])
        self.taskPanel.grid(row=1, column=3)

    def DefaultConfig(self):
        # self.root.geometry("{width}x{height}".format(width=900, height=600))
        
        font.nametofont("TkDefaultFont").config(size=12)    # Default font
        font.nametofont("TkTextFont").config(size=12)       # Textbox font

    def GridConfig(self):

        col_count, row_count = self.root.grid_size()

        # for col in range(col_count):
        #     self.root.grid_columnconfigure(col, weight=1)

        for row in range(row_count):
            self.root.grid_rowconfigure(row, minsize=10)

    def NextPage(self):
        self.currentPageIndex = (self.currentPageIndex + 1) % len(self.pages)
        self.UpdatePageButtons()

    def PrevPage(self):
        self.currentPageIndex = (self.currentPageIndex + len(self.pages) - 1) % len(self.pages)
        self.UpdatePageButtons()

    def ViewerSetup(self):
        
        # Pokedex Pane
        self.pokedexPanel = PanedWindow(self.root)
        self.pokedexEntry = PokedexEntry(self.pages[self.currentPageIndex], self.pokedexPanel)
        
        # Research Task Pane
        self.taskPanel = PanedWindow(self.root)
        self.taskEntry = ResearchTaskManager(self.taskPanel, self.pages[self.currentPageIndex])

        self.prevButton = Button(self.root, text="上一頁", command=self.PrevPage)
        self.nextButton = Button(self.root, text="下一頁", command=self.NextPage)
        self.UpdatePageButtons()

    def ViewerLayout(self):

        self.pokedexPanel.grid(row=1, column=2)
        self.taskPanel.grid(row=1, column=3)
        self.prevButton.grid(row=2, column=1)
        self.nextButton.grid(row=2, column=4)
    
    def Centering(self):
        col_count, row_count = self.root.grid_size()

        Label(self.root).grid(row=0, column=0, sticky=NSEW)
        Label(self.root).grid(row=0, column=col_count, sticky=NSEW)
        Label(self.root).grid(row=row_count, column=0, sticky=NSEW)
        Label(self.root).grid(row=row_count, column=col_count, sticky=NSEW)

        self.root.grid_rowconfigure(0, weight=1)
        self.root.grid_rowconfigure(row_count, weight=1)
        self.root.grid_columnconfigure(0, weight=1)
        self.root.grid_columnconfigure(col_count, weight=1)

    def RunWindow(self):
        self.root.mainloop()