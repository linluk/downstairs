#!/usr/bin/env python3

import ui

import game
import menu
import intro
import inventory
import state_manager

try:

    try:
        ui.start()
        ui.commands.init_commands()
        g = game.Game()
        m = menu.Menu()
        intro = intro.Intro()
        i = inventory.Inventory()


        m.add_item('Start', game.Game)
        m.add_item('Quit', None)

        sm = state_manager.StateManager()
        sm.add_state(m)
        sm.add_state(g)
        sm.add_state(i)
        sm.add_state(intro)

        sm.change_state(menu.Menu)

        sm.main_loop()

        #ch = ui.getch()
        #while ch != ord(' '):
        #    ui.clear()
        #    ui.addch(3, 3, str(ch))
        #    ch = ui.getch()


    finally:
        ui.stop()

except:
    print('Something went terribly wrong...')
    print('let me gather some information about it.')
    import bugreport
    brf = bugreport.bugreport()
    print('I created a bugreport in: "{}"'.format(brf))
    print('It would really help when you send it over to MAILING LIST!')
    print('')

print('Thanks for playing :-)')

