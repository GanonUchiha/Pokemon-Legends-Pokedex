
from pathlib import Path
import json

class CompletionData:

    debug = False

    def __init__(self, pokedexDir: Path):
        self.filepath = pokedexDir.joinpath("completion.json")

        self.LoadData()
    
    def InitData(self, number, length: int) -> None:
        number = "{:03}".format(int(number))
        self.data[number] = [0 for i in range(length)]
    
    def HasData(self, number) -> bool:
        number = "{:03}".format(int(number))
        return number in self.data

    def GetData(self, number) -> list[int]:
        number = "{:03}".format(int(number))
        if not self.HasData(number):
            raise Exception("There is not data for {}. Initialize the data first.".format(number))
        return self.data[number]
    
    def SetData(self, number, newData: list[int]) -> None:
        number = "{:03}".format(int(number))
        self.data[number] = newData
    
    def LoadData(self):

        if self.filepath.exists():
            with self.filepath.open(encoding="utf-8") as fp:
                self.data = json.load(fp)
        else:
            print("No data found. Initalizing empty data.")
            self.data = dict[str, list[int]]()
    
    def SaveData(self):
        if self.filepath.exists():
            print("Overwriting data")
        else:
            print("Creating data save")
        
        if self.debug:
            print(self.data)

        with self.filepath.open("w", encoding="utf-8") as fp:
            json.dump(
                self.data,
                fp,
                ensure_ascii=False,
                sort_keys=True,
                indent="\t"
            )