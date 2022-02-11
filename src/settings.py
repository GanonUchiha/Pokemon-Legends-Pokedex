
# Standard Libraries
from pathlib import Path

# Other modules
from CompletionData import CompletionData

POKEDEX_DIR = Path("./pokedex")
IMAGES_DIR = Path("./images")
TESSERACT_EXE_PATH = r"C:\Program Files\Tesseract-OCR\tesseract.exe"
BTN_TEXT_UPDATE = "更新"

PKMN_NAME       = "名稱"
PKMN_CATEGORY   = "類別"
PKMN_TYPE       = "屬性"
PKMN_FOOD       = "愛吃的食物"
PKMN_FOOD_TYPES = ["菇", "蜜", "穀", "豆", "礦"]
PKMN_HOLDITEM   = "持有物"

PKMN_TASK       = "圖鑑課題"
TASK_DESCR      = "說明"
TASK_LEVEL      = "階段"

COMPLETION_DATA = CompletionData(POKEDEX_DIR)