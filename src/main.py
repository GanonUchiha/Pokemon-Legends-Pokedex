import tkinter as tk
from tkinter import font

# Global vairables
from settings import *

from Pokedex import Pokedex

def main():

    myPokedex = Pokedex()
    myPokedex.RunWindow()

if __name__ == "__main__":
    main()