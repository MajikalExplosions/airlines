# Name: Runner.py
# Description: Runner program.

# Ver.	    Writer			        Date			Notes
# 1.0   Christopher Luey            05/17/20		Original


import GUI

def main():
    gui = GUI.GUI()
    clicked = 0
    while clicked != "quit":
        screen = gui.getScreen()
        clicked = gui.setOnButtonClickListener()
        print(clicked)
        if clicked == 'quit':
            break
        gui.switchScreen(clicked)

if __name__ == '__main__':
    main()
