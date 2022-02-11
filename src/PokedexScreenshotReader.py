
# Standard Libraries
from PIL import Image, ImageEnhance
from pathlib import Path

# Other Libraries
import pytesseract

from settings import IMAGES_DIR, TESSERACT_EXE_PATH

pytesseract.pytesseract.tesseract_cmd = TESSERACT_EXE_PATH

class EntryNotFoundException(Exception):

    message = "Pokedex image of {page} page not found for No. {number:03} "

    def __init__(self, number, page: str):            
        # Call the base class constructor with the parameters it needs
        super().__init__(self.message.format(number=int(number), page=page))

class PokedexScreenshotReader():

    debug = True

    def __init__(self):
        pass

    @classmethod
    def ReadTaskFromImage(self, number) -> list:
        
        imagePath: Path = IMAGES_DIR.joinpath("tasks", "{:03}.jpg".format(int(number)))

        # Detect if image exists
        if not imagePath.exists():
            raise EntryNotFoundException(number, "Tasks")

        # Open image
        image: Image.Image = Image.open(imagePath)

        # Get task descriptions
        imageCropped: Image.Image = image.crop((85, 135, 520, 530)).convert('L')
        taskDescr: str = pytesseract.image_to_string(imageCropped, lang='chi_tra', config="--psm 6")
        taskDescrList = self.StrToList(taskDescr)

        # Get taks completion count
        numberImageCropped: Image.Image = image.crop((520, 135, 570, 530))
        taskCount: str = pytesseract.image_to_string(numberImageCropped, lang='eng', config="--psm 6 digit")
        taskCountList = [int(count) for count in self.StrToList(taskCount)]

        # Get taks completion levels
        taskLevelList = self.GetTaskLevels(image, 580, 140)

        return self.MergeLists([taskDescrList, taskCountList, *taskLevelList])
    
    # Remove as much red from the image as possible
    @classmethod
    def RemoveRed(self, img: Image.Image):

        def IsRed(color: tuple[int, int, int]) -> bool:
            threshold = 70
            if 255 - color[0] <= threshold:
                return True
            if color[0] > 100 and color[1] < threshold and color[2] < threshold:
                return True
            return False

        # Get the size of the image
        width, height = img.size

        # Process every pixel
        for x in range(width):
            for y in range(height):
                currentColor = img.getpixel( (x,y) )
                newColor = (251, 227, 89)
                if IsRed(currentColor):
                    img.putpixel( (x,y), newColor)
        return img

    @classmethod
    def GetTaskLevels(self, img: Image.Image, left: int, up: int) -> list[list[str]]:

        taskLevelList: list[list[str]] = list()
        for i in range(5):
            l = left + 55 * i
            u = up
            r = left + 55 * i + 50
            d = up + 387

            levelImageCropped: Image.Image = img.crop((l, u, r, d))
            levelImageContrast: ImageEnhance.Contrast = ImageEnhance.Contrast(levelImageCropped)
            levelImageCropped = self.RemoveRed(levelImageContrast.enhance(3))
            # levelImageCropped.show()
            taskLevel: str = pytesseract.image_to_string(levelImageCropped, lang='eng', config="--psm 6")
            if self.debug:
                print(taskLevel)

            taskLevelList.append([int(num) for num in self.StrToList(taskLevel)])
        
        return taskLevelList
    
    @classmethod
    def StrToList(self, s: str, excludeEmpty: bool = True) -> list[str]:
        if excludeEmpty:
            return [subStr for subStr in s.split("\n") if subStr != ""]
        else:
            return [subStr for subStr in s.split("\n")]
    
    @classmethod
    def MergeLists(self, lists: list[list]) -> list:
        
        numTasks = max([len(l) for l in lists])
        if self.debug:
            print(lists)
            print(numTasks)

        for i in range(len(lists)):
            diff = numTasks - len(lists[i])
            
            if diff > 0:
                if type(lists[i][0]) is int:
                    lists[i].extend([0 for i in range(diff)])
                else:
                    lists[i].extend(["N/A" for i in range(diff)])

        return zip(*lists)

    @classmethod
    def ReadSummaryFromImage(self, number) -> dict:
        
        imagePath: Path = IMAGES_DIR.joinpath("summary", "{:03}.jpg".format(int(number)))

        # Detect if image exists
        if not imagePath.exists():
            raise EntryNotFoundException(number, "Summary")

        # Open image
        image: Image.Image = Image.open(imagePath)

        # Get name
        imageCropped = image.crop((170, 84, 258, 118))
        imageContrast: ImageEnhance.Contrast = ImageEnhance.Contrast(imageCropped)
        name: str = pytesseract.image_to_string(imageCropped, lang='chi_tra', config="--psm 6").strip()
        if self.debug:
            print("Name: {}".format(name))

        # Get category
        imageCropped = image.crop((390, 90, 600, 115))
        imageContrast: ImageEnhance.Contrast = ImageEnhance.Contrast(imageCropped)
        category: str = pytesseract.image_to_string(imageCropped, lang='chi_tra', config="--psm 6").strip()
        category = category.replace("寶可夢", "")
        if self.debug:
            print("Category: {}".format(category))

        # Get Type
        imageCropped = image.crop((661, 90, 711, 115))
        imageContrast: ImageEnhance.Contrast = ImageEnhance.Contrast(imageCropped)
        type1: str = pytesseract.image_to_string(imageContrast.enhance(2), lang='chi_tra', config="--psm 6").strip()

        imageCropped = image.crop((775, 90, 813, 115))
        imageContrast: ImageEnhance.Contrast = ImageEnhance.Contrast(imageCropped)
        type2: str = pytesseract.image_to_string(imageContrast.enhance(3), lang='chi_tra', config="--psm 6").strip()

        types = [t for t in (type1, type2) if t != ""]
        if self.debug:
            print("Types: {}".format(types))

        # Get Food
        food: list[str] = self.GetFood(image)

        # Get items
        imageCropped = image.crop((621, 363, 742, 388))
        imageContrast: ImageEnhance.Contrast = ImageEnhance.Contrast(imageCropped)
        item1: str = pytesseract.image_to_string(imageContrast.enhance(2), lang='chi_tra', config="--psm 6").strip()

        imageCropped = image.crop((621, 396, 742, 420))
        imageContrast: ImageEnhance.Contrast = ImageEnhance.Contrast(imageCropped)
        item2: str = pytesseract.image_to_string(imageContrast.enhance(2), lang='chi_tra', config="--psm 6").strip()

        items = [t for t in (item1, item2) if t != ""]
        if self.debug:
            print("Items: {}".format(items))
        

        summary: dict = {
            "Name": name,
            "Category": category,
            "Types": types,
            "Food": food,
            "Items": items
        }
        return summary

    @classmethod
    def GetFood(self, img: Image.Image) -> list:
        referenceColor: tuple[int, int, int] = (236, 231, 209)
        threshold: int = 35

        def DiffOfSum(tuple1, tuple2):
            return abs(sum(tuple1) - sum(tuple2))
        
        foodList: list[str] = list()

        if self.debug:
            print(DiffOfSum(img.getpixel( (650, 290) ), referenceColor))
        
        if DiffOfSum(img.getpixel( (650, 290) ), referenceColor) > threshold:
            foodList.append("菇")
        if DiffOfSum(img.getpixel( (690, 290) ), referenceColor) > threshold:
            foodList.append("蜜")
        if DiffOfSum(img.getpixel( (725, 290) ), referenceColor) > threshold:
            foodList.append("穀")
        if DiffOfSum(img.getpixel( (770, 290) ), referenceColor) > threshold:
            foodList.append("豆")
        if DiffOfSum(img.getpixel( (795, 290) ), referenceColor) > threshold:
            foodList.append("礦")
        
        return foodList

def main():

    number = input("Give a number: ")
    print(int(number))
    while number.isdigit():
        summary = PokedexScreenshotReader.ReadSummaryFromImage(number)
        print(summary)
        tasks = PokedexScreenshotReader.ReadTaskFromImage(number)
        print(list(tasks))
        number = input("Give a number: ")

if __name__ == "__main__":
    main()