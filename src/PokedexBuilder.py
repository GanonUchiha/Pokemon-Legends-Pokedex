
# Standard Libraries
import json
from pathlib import Path
import traceback

# Other modules
from settings import *
from PokedexScreenshotReader import PokedexScreenshotReader as Reader, EntryNotFoundException

class PokedexBuilder:

    def __init__(self):
        pass

    @classmethod
    def UpdateEntryTasks(self, number, tasks: list[list], overwriteTasks: bool = False):
        entryPath: Path = POKEDEX_DIR.joinpath("{:03}.json".format(int(number)))

        if entryPath.exists():
            data = json.load(entryPath.open(encoding="utf-8"))
        else:
            data = dict()
        
        if PKMN_TASK in data and not overwriteTasks:
            raise Exception("Tasks existed. Set option \"overwriteTasks\" to True to overwrite.")

        data[PKMN_TASK] = list()
        for task in tasks:
            taskDict = {
                TASK_DESCR: task[0],
                TASK_LEVEL: [x for x in task[2:] if x > 0]
            }
            data[PKMN_TASK].append(taskDict)
        
        json.dump(
            data,
            entryPath.open("w", encoding="utf-8"),
            ensure_ascii=False,
            sort_keys=True,
            indent="\t"
        )

    @classmethod
    def UpdateEntrySummary(self, number, summary: dict, overwriteInfo: bool = False):
        entryPath: Path = POKEDEX_DIR.joinpath("{:03}.json".format(int(number)))

        if entryPath.exists():
            data = json.load(entryPath.open(encoding="utf-8"))
        else:
            data = dict()

        data["No."] = "{:03}".format(int(number))

        keys = [
            (PKMN_NAME, "Name"),
            (PKMN_CATEGORY, "Category"),
            (PKMN_TYPE, "Types"),
            (PKMN_FOOD, "Food"),
            (PKMN_HOLDITEM, "Items")
        ]

        for (key1, key2) in keys:

            if key1 not in data and not overwriteInfo:
                print("property {} skipped. Set option \"overwriteTasks\" to True to overwrite.".format(key2))
            
            data[key1] = summary[key2]
        
        json.dump(
            data,
            entryPath.open("w", encoding="utf-8"),
            ensure_ascii=False,
            sort_keys=True,
            indent="\t"
        )

def main():

    for i in range(1, 300):
        try:
            print("Summary for", i)
            PokedexBuilder.UpdateEntrySummary(i, Reader.ReadSummaryFromImage(i))

            print("Tasks for", i)
            PokedexBuilder.UpdateEntryTasks(i, Reader.ReadTaskFromImage(i))
        except EntryNotFoundException:
            continue
        except Exception:
            traceback.print_exc()
            continue

if __name__ == "__main__":
    main()