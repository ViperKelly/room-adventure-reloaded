# Name: Russell Kelly
# Date: 3/29/2023
# Description: Room Adventure Revolutions

from tkinter import *


class Room:
    """A Room has a name and a filepath that points to a .gif image"""

    def __init__(self, name: str, image_filepath: str) -> None:
        self.name = name
        self.image = image_filepath
        self.exits = {}
        self.items = {}
        self.grabs = []

    def add_exit(self, label: str, room: 'Room'):
        self.exits[label] = room

    def add_item(self, label: str, desc: str):
        self.items[label] = desc

    def add_grabs(self, label: str):
        self.grabs.append(label)

    def del_grabs(self, label:str):
        self.grabs.remove(label)

    def __str__(self) -> str:
        # Create the base response
        result = f"You are in {self.name}\n"

        # append the items you see in the room
        result += f"You see: "
        for item in self.items.keys():
            result += item + " "
        result += "\n"

        # append the exits available in the room
        result += "Exits: "
        for exit in self.exits.keys():
            result += exit + " "
        result += "\n"

        return result


class Game:
    pass

