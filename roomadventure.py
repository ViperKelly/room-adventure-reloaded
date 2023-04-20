# Name: Kieran
# Date: 3/29/2023
# Description: Room Adventure Revolutions

from tkinter import *
from random import randint, choice
import time

breads = {}  # Creates Bread dictionary to access breads as a point system


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

    def del_grabs(self, label: str):
        self.grabs.remove(label)

    # adds bread to the bread dictionary and to the grabs list by the add_grabs function
    def add_breads(self, label: str, points: int):
        breads[label] = points
        self.add_grabs(label)

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


class Game(Frame, Room):
    EXIT_ACTIONS = ["quit", "exit", "bye", "q"]

    # Statuses
    STATUS_DEFAULT = "I don't understand. Try [veb] [noun]. Valid bers are go, look, take, eat."
    STATUS_DEAD = "You are dead."
    STATUS_BAD_EXIT = "Invalid Exit."
    STATUS_ROOM_CHANGE = "Room Changed"
    STATUS_GRABBED = "Item Grabbed"
    STATUS_BAD_GRABS = "I can't grab that."
    STATUS_BAD_ITEM = "I don't see that."
    STATUS_BAD_EAT = "Why would you eat that"
    STATUS_GOOD_EAT = "I LOVE BREAD!!!"
    STATUS_TIME_UP = "Your Time is Up"

    WIDTH = 800
    HEIGHT = 600

    def __init__(self, parent):
        self.inventory = []
        self.points: int = 0
        Frame.__init__(self, parent)
        self.pack(fill=BOTH, expand=1)

    def setup_game(self):

        self.rooms = []
        # create rooms
        r1 = Room("Room 1", "room1.gif")
        r2 = Room("Room 2", "room2.gif")
        r3 = Room("Room 3", "room3.gif")
        r4 = Room("Room 4", "room4.gif")
        r5 = Room("Room 5", "room5.gif")
        r6 = Room("Room 6", "room6.gif")
        self.rooms = [r1, r2, r3, r4, r5, r6]  # append list when new room created

        # add exits to the rooms
        r1.add_exit("east", r2)
        r1.add_exit("south", r3)

        r2.add_exit("west", r1)
        r2.add_exit("south", r4)

        r3.add_exit("north", r1)
        r3.add_exit("east", r4)
        r3.add_exit("south", r6)

        r4.add_exit("north", r2)
        r4.add_exit("west", r3)
        r4.add_exit("south", None)  # None means death
        r4.add_exit("east", r5)

        r5.add_exit("west", r4)

        r6.add_exit("north", r3)

        # add items to the rooms
        r1.add_item("chair", "Something about wicker and legs")
        r1.add_item("bigger_chair", "More wicker and more legs")

        r2.add_item("fireplace", "It is made of fire. Grab some fire and bring it with you.")
        r2.add_item("more_chair", "another chair named more.")

        r3.add_item("desk", "It is made of wicker also. A wicker desk. No one is sitting on it.")
        r3.add_item("dimsdale_dimadome", "Owned by Doug Dimadome, \
                     owner of the Dimsdale Dimadome. Thats right.")

        r4.add_item("croissant", "It is made of butter. No flour.")

        r5.add_item("statue", "A statue of Gabe Newell")

        r6.add_item("toybox", "Inside is a limited edition 2011 Bionicle")

        # add grabs to the rooms
        r1.add_grabs("key")
        r1.add_grabs("femur")
        r2.add_grabs("fire")
        r2.add_grabs("knife")
        r3.add_grabs("Stretch_Armstrong")
        r4.add_grabs("butter")
        r4.add_grabs("margarine")

        r5.add_grabs("snail")
        r6.add_grabs("raisin")

        # add breads to rooms
        r1.add_breads("bagel1", randint(100, 250))
        r1.add_breads("white", 50)
        r2.add_breads("bagel2", randint(100, 250))
        r2.add_breads("baguette", 150)
        r3.add_breads("bagel3", randint(100, 250))
        r3.add_breads("croissant", 225)
        r4.add_breads("wholewheat", 150)
        r4.add_breads("pumpernickel", 500)
        r5.add_breads("cornbread", 350)
        r5.add_breads("brioche", 275)
        r6.add_breads("ciabatta", 175)
        r6.add_breads("sourdough", 190)

        # set the current room to the starting room
        self.current_room = r1


    def setup_gui(self):
        self.player_input = Entry(self, bg="white", fg="black")
        self.player_input.bind("<Return>", self.process)
        self.player_input.pack(side=BOTTOM, fill=X)
        self.player_input.focus()

        # the image container and default image
        img = None  # represents the actual image
        self.image_container = Label(self, width=Game.WIDTH // 2, image=img)
        self.image_container.pack(side=LEFT, fill=Y)
        self.image_container.image = img  # ensuring image persistence after function ends
        # prevent the image from modifying the size of the container it is in
        self.image_container.pack_propagate(False)

        # container for the game text
        text_container = Frame(self, width=Game.WIDTH // 2)
        self.text = Text(text_container, bg="lightgray", fg="black", state=DISABLED)
        self.text.pack(fill=Y, expand=1)
        text_container.pack(side=RIGHT, fill=Y)
        text_container.pack_propagate(False)

    def set_room_image(self):
        if self.current_room is None:
            img = PhotoImage(file="skull.gif")
        else:
            img = PhotoImage(file=self.current_room.image)

        self.image_container.config(image=img)
        self.image_container.image = img

    def set_status(self, status):
        self.text.config(state=NORMAL)  # make it editable
        self.text.delete(1.0, END)  # yes 1.0 not 0 for Entry elements
        if self.current_room is None:
            self.text.insert(END, Game.STATUS_DEAD)
        else:
            content = f"{self.current_room}\nYou are carrying: {self.inventory}\nThings that stick out: {self.current_room.grabs}\nYour Score: {self.points}\n\n{status}"
            self.text.insert(END, content)

        self.text.config(state=DISABLED)  # no longer editable

    def clear_entry(self):
        self.player_input.delete(0, END)

    def handle_go(self, destination):
        status = Game.STATUS_BAD_EXIT

        if destination in self.current_room.exits:
            self.current_room = self.current_room.exits[destination]
            status = Game.STATUS_ROOM_CHANGE

        self.set_status(status)
        self.set_room_image()

    def handle_look(self, item):
        status = Game.STATUS_BAD_ITEM

        if item in self.current_room.items:
            status = self.current_room.items[item]

        self.set_status(status)

    def handle_take(self, grabbable):
        status = Game.STATUS_BAD_GRABS

        if grabbable in self.current_room.grabs:
            self.inventory.append(grabbable)
            self.current_room.del_grabs(grabbable)
            status = Game.STATUS_GRABBED

        self.set_status(status)

    # EAT Grabbables (please eat bread): adds a point system based on what you eat
    def handle_eat(self, grabbable):
        status = None

        if grabbable in self.inventory:
            # makes sure item is a bread
            if grabbable in breads:
                self.points += breads[grabbable] # thank goodness you eat bread here is points
                self.random_room = choice(self.rooms)
                self.inventory.remove(grabbable)
                self.random_room.add_grabs(grabbable)
                status = Game.STATUS_GOOD_EAT
            else:
                self.points -= 250  # why did you eat that give me the points back
                self.random_room = choice(self.rooms)
                self.inventory.remove(grabbable)
                self.random_room.add_grabs(grabbable)
                status = Game.STATUS_BAD_EAT
        self.set_status(status)

    def play(self):
        self.setup_game()
        self.setup_gui()
        self.set_room_image()
        self.set_status("")

    # function that checks if you have dropped some items!(you are missing fingers
    def dropped(self, inventory):

        if len(inventory) >= 2:
            num = randint(1, 5)

            if num == 3:
                num2 = randint(0, (len(inventory) - 1))
                print(num2)
                status = f"Welp, your missing fingers didn't help you there. You dropped your {self.inventory[num2]}"
                self.current_room.add_grabs(self.inventory[num2])
                self.inventory.remove(self.inventory[num2])
                self.points -= 100
                self.set_status(status)

    def process(self, event):
        action = self.player_input.get()
        action = action.lower()

        if action in Game.EXIT_ACTIONS:
            exit()

        if self.current_room is None:
            self.clear_entry()
            return

        words = action.split()

        if len(words) != 2:
            self.set_status(Game.STATUS_DEFAULT)
            return

        self.clear_entry()

        verb = words[0]
        noun = words[1]

        match verb:
            case "go":
                self.handle_go(destination=noun)
            case "look":
                self.handle_look(item=noun)
            case "take":
                self.handle_take(grabbable=noun)
            case "eat":
                self.handle_eat(grabbable=noun)

        self.dropped(self.inventory)
        print(self.current_room.grabs)


# Main
window = Tk()
window.title("Room Adventure... REVOLUTIONS")
game = Game(window)
game.play()
window.mainloop()
