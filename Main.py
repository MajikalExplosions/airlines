# Name: Main.py
# Description: Runner program.

# Ver.	    Writer			        Date			Notes
# 1.0       Christopher Luey        05/17/20		Original
# 1.1       Christopher Luey        05/17/20		Compatibility with widget id system


from UI import GUI


def main():
    gui = GUI.GUI()
    clicked = 0
    screens = gui.getScreenIDs()
    while clicked != 'quit':
        screen = gui.getScreen()
        clicked = gui.setOnButtonClickListener()
        if clicked == 'quit':
            break
        print("ID:", clicked, "- Action Performed")
        if clicked in screens or clicked == 'back':
            gui.switchScreen(clicked)
        else:
            print("ID:", clicked, "- Not Switch Screen")


if __name__ == '__main__':
    main()
