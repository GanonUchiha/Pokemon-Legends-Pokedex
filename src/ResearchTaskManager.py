
# Standard Libraries
from tkinter import Button, Label
import json

# Other modules
from settings import *
from Viewer import Viewer
from ResearchTask import ResearchTask

class ResearchTaskManager(Viewer):

    title = "圖鑑課題"
    
    def __init__(self, root, number, startRow: int=0, startCol: int=0):

        self.root = root
        self.number = number

        self.TasksSetup()
        self.SetStartPos(startRow, startCol)
    
    def TasksSetup(self):
        pokedexFilename = "{:03}.json".format(int(self.number))
        pokedexFilePath = POKEDEX_DIR.joinpath(pokedexFilename)
        data = json.load(pokedexFilePath.open(encoding="utf-8"))
        
        self.GetTasksFromData(data[PKMN_TASK])

        self.taskCompletion = list[int]()
        try:
            self.taskCompletion = COMPLETION_DATA.GetData(self.number)
            if len(self.taskCompletion) != self.numTasks:
                raise Exception("Number of counters don't match the number of tasks")
        except Exception:
            COMPLETION_DATA.InitData(self.number, self.numTasks)
            self.taskCompletion = COMPLETION_DATA.GetData(self.number)

    def ReadCountFromData(self):
        for index, task in enumerate(self.tasks):
            task.ReadCountFromData(self.taskCompletion[index])

    def WriteCountToData(self):
        for index, task in enumerate(self.tasks):
            task.UpdateCount()
            self.taskCompletion[index] = task.count

        COMPLETION_DATA.SetData(self.number, self.taskCompletion)
        COMPLETION_DATA.SaveData()

    def ViewerSetup(self):

        # Title
        self.titleLabel = Label(self.root, text=self.title)

        # Update Count
        self.updateBtn = Button(self.root, text=BTN_TEXT_UPDATE, command=self.WriteCountToData)

        # Tasks
        ## TODO: setup for all tasks
        for task in self.tasks:
            task.ViewerSetup()
        self.ReadCountFromData()
            

    def ViewerLayout(self):

        # Title
        self.titleLabel.grid(row=self.startRow, column=self.startCol)
        
        # Update Count
        self.updateBtn.grid(row=self.startRow, column=self.startCol + 1)

        # Tasks
        ## TODO: setup layout for all tasks
        for index, task in enumerate(self.tasks):
            row = self.startRow + index + 1
            col = self.startCol
            task.SetStartPos(row, col)
            task.ViewerLayout()

    def GetTasksFromData(self, tasksData: list[dict]) -> None:
        self.tasks = list[ResearchTask]()

        for taskData in tasksData:
            description = taskData[TASK_DESCR]
            levels = taskData[TASK_LEVEL]
            task = ResearchTask(self.root, description, levels)
            self.tasks.append(task)
        
        self.numTasks = len(self.tasks)