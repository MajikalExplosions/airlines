# File: 
# Written By: Christopher Luey
# Date: 
# 

import GUI

def main():
    gui = GUI.GUI()
    clicked = gui.setOnButtonClickListener()
    while clicked != "quit":
        screen = gui.getScreen()
        clicked = gui.setOnButtonClickListener()

main()
