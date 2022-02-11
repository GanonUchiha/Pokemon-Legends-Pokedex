
# Standard Libraries
import abc

class Viewer(abc.ABC):
    
    def SetStartPos(self, startRow: int, startCol: int) -> None:
        self.startRow = startRow
        self.startCol = startCol

    @abc.abstractmethod
    def ViewerSetup(self):
        pass

    @abc.abstractmethod
    def ViewerLayout(self):
        pass