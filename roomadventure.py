# Name: Kieran
# Date: 3/29/2023
# Description: Room Adventure Revolutions

from tkinter import *
from random import randint

locked = True

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



class Game(Frame):
    EXIT_ACTIONS = ["quit", "exit", "bye", "q"]

    # Statuses
    STATUS_DEFAULT = "I don't understand. Try [veb] [noun]. Valid bers are go, look, take."
    STATUS_DEAD = "You are dead."
    STATUS_BAD_EXIT = "Invalid Exit."
    STATUS_ROOM_CHANGE = "Room Changed"
    STATUS_GRABBED = "Item Grabbed"
    STATUS_BAD_GRABS = "I can't grab that."
    STATUS_BAD_ITEM = "I don't see that."

    WIDTH = 800
    HEIGHT = 600

    def __init__(self, parent):
        self.inventory = []
        Frame.__init__(self, parent)
        self.pack(fill=BOTH, expand=1)

    def setup_game(self):

        # create rooms
        r1 = Room("Room 1", "room1.gif")
        r2 = Room("Room 2", "room2.gif")
        r3 = Room("Room 3", "room3.gif")
        r4 = Room("Room 4", "room4.gif")

        r5 = Room("Room 5", "room5.gif")
        r6 = Room("Room 6", "room6.gif")

        r7 = Room("the outside world", "forest.png")

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

        r5.add_exit("east", r7)

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
        r5.add_item("door", "A locked door. Maybe there's a key around here somewhere")

        r6.add_item("toybox", "Inside is a limited edition 2011 Bionicle")

        r7.add_item("forest", "A forest. You are finally free.")

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

        # set the current room to the starting room
        self.current_room = r1

    def setup_gui(self):
        self.player_input = Entry(self, bg="white", fg="black")
        self.player_input.bind("<Return>", self.process)
        self.player_input.pack(side=BOTTOM, fill=X)
        self.player_input.focus()

        # the image container and default image
        img = None  # represents the acutal image
        self.image_container = Label(self, width=Game.WIDTH // 2, image=img)
        self.image_container.pack(side=LEFT, fill=Y)
        self.image_container.image = img  # ensuring image persistance after function ends
        # prevent the image from modifying the size of the container it is in
        self.image_container.pack_propagate(False)

        # container for the game text
        text_container = Frame(self, width=Game.WIDTH // 2)
        self.text = Text(text_container, bg="lightgray", fg="black", state=DISABLED)
        self.text.pack(fill=Y, expand=1)
        text_container.pack(side=RIGHT, fill=Y)
        text_container.pack_propagate(False)

    def set_room_image(self):
        if self.current_room == None:
            img = PhotoImage(file="skull.gif")
        else:
            img = PhotoImage(file=self.current_room.image)

        self.image_container.config(image=img)
        self.image_container.image = img

    def set_status(self, status):
        self.text.config(state=NORMAL)  # make it editable
        self.text.delete(1.0, END)  # yes 1.0 not 0 for Entry elements
        if self.current_room == None:
            self.text.insert(END, Game.STATUS_DEAD)

        else:
            content = f"{self.current_room}\nYou are carrying: {self.inventory}\nThings that stick out: {self.current_room.grabs}\n\n{status}"
            self.text.insert(END, content)

        self.text.config(state=DISABLED)  # no longer editable

    def clear_entry(self):
        self.player_input.delete(0, END)

    def handle_go(self, destination):
        status = Game.STATUS_BAD_EXIT

        if destination in self.current_room.exits:
            # check if player is in room 5. If so, checks if the east door is locked before switching rooms.
            if ((destination == "east") & (locked == False) & (self.current_room.name == "Room 5")):
                status = "You have escaped into the forest and won the game. Thanks for playing"
                self.current_room = self.current_room.exits[destination]
                self.set_room_image()
            elif((self.current_room.name == "Room 5") & (destination != "east")):
                self.current_room = self.current_room.exits[destination]
                status = Game.STATUS_ROOM_CHANGE
                self.set_room_image()
            elif self.current_room.name != "Room 5":
                self.current_room = self.current_room.exits[destination]
                status = Game.STATUS_ROOM_CHANGE
                self.set_room_image()
            else:
                status = "The door is locked, maybe I can find a key"
            self.set_status(status)
        

    def handle_look(self, item):
        status = Game.STATUS_BAD_ITEM

        if item in self.current_room.items:
            status = self.current_room.items[item]

        self.set_status(status)

    def handle_take(self, grabbable):
        global locked
        
        status = Game.STATUS_BAD_GRABS

        if grabbable in self.current_room.grabs:

            if grabbable == "key":
                locked = False
            self.inventory.append(grabbable)
            self.current_room.del_grabs(grabbable)
            status = Game.STATUS_GRABBED
            

        self.set_status(status)

    def play(self):
        self.setup_game()
        self.setup_gui()
        self.set_room_image()
        self.set_status("")
        
    #function that checks if you have dropped some items!(you are missing fingers
    def dropped(self, inventory):

        if len(inventory) >=2:
            num = randint(1,5)

            if num == 3:
                num2 = randint(0, (len(inventory)-1))
                print(num2)
                status = (f"Welp, your missing fingers didn't help you there. You dropped your {self.inventory[num2]}")
                self.current_room.add_grabs(self.inventory[num2])
                self.inventory.remove(self.inventory[num2])
                self.set_status(status)

    def process(self, event):
        action = self.player_input.get()
        action = action.lower()

        if action in Game.EXIT_ACTIONS:
            exit()

        if self.current_room == None:
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

        self.dropped(self.inventory)
        print(self.current_room.grabs)




# Main
window = Tk()
window.title("Room Adventure... REVOLUTIONS")
game = Game(window)
game.play()
window.mainloop()
