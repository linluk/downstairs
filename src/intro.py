import ui
import defs

import state

import time

class Intro(state.State):
    def __init__(self):
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
