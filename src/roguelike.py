#!/usr/bin/env python3

import ui

import game

import state_manager

try:

  ui.start()
  ui.commands.init_commands()

  g = game.Game()

  sm = state_manager.StateManager()
  sm.add_state(g)
  sm.main_loop()

finally:
  ui.stop()

print('Thanks for playing :-)')

