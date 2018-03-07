#!/usr/bin/env python3

import ui
import defs

import state
import game
import menu

import inventory
import state_manager
import time


class Intro(state.State):
    def __init__(self):
        super().__init__()
        self.f_color = (255, 255, 255)
        self.title = """
███████╗██╗  ██╗ █████╗ ██████╗  ██████╗ ██╗    ██╗███████╗████████╗███████╗██████╗\n
██╔════╝██║  ██║██╔══██╗██╔══██╗██╔═══██╗██║    ██║██╔════╝╚══██╔══╝██╔════╝██╔══██╗\n
███████╗███████║███████║██║  ██║██║   ██║██║ █╗ ██║███████╗   ██║   █████╗  ██████╔╝\n
╚════██║██╔══██║██╔══██║██║  ██║██║   ██║██║███╗██║╚════██║   ██║   ██╔══╝  ██╔═══╝\n
███████║██║  ██║██║  ██║██████╔╝╚██████╔╝╚███╔███╔╝███████║   ██║   ███████╗██║\n
╚══════╝╚═╝  ╚═╝╚═╝  ╚═╝╚═════╝  ╚═════╝  ╚══╝╚══╝ ╚══════╝   ╚═╝   ╚══════╝╚═╝\n"""

        self.sub_title = 'Beyond Darkness'

    def render(self) -> None:
        ui.clear()
        y = (defs.SCREEN_H // 2) - (defs.SCREEN_W // 2)
        i = 0
        lines = self.title.splitlines()
        for line in lines:
            i += 8
            ui.draw_intro(line, 0, i)
            time.sleep(100)

    def update(self) -> None:
        pass

    def leave(self) -> None:
        pass

    def enter(self) -> None:
        ui.clear()


if __name__ == '__main__':
    try:

        ui.start()
        ui.commands.init_commands()
        g = game.Game()
        m = menu.Menu()
        intro = Intro()
        i = inventory.Inventory()

        m.add_item('Start', game.Game)
        m.add_item('Quit', None)

        sm = state_manager.StateManager()
        sm.add_state(intro)
        sm.add_state(m)
        sm.add_state(g)
        sm.add_state(i)


        sm.change_state(Intro)

        sm.main_loop()


    finally:
        ui.stop()
