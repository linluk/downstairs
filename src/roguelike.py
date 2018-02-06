#!/usr/bin/env python3

import ui

import game
import menu

import state_manager

try:

  ui.start()
  ui.commands.init_commands()

  g = game.Game()
  m = menu.Menu()
  m.add_item('Start', game.Game)
  m.add_item('Quit', None)

  sm = state_manager.StateManager()
  sm.add_state(m)
  sm.add_state(g)
  sm.change_state(menu.Menu)

  sm.main_loop()

finally:
  ui.stop()

print('Thanks for playing :-)')

