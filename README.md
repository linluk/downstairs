README
======

Author: Lukas Singer

Created: 2017-10-04

License: [WTFPL](http://www.wtfpl.net/)

This project should become a
[Roguelike](http://en.wikipedia.org/wiki/Roguelike) Game and/or an Engine.

Setup
=====

```
# create a virtual environment with python3
python3 -m venv venv

# activate the virtual environment
. venv/bin/activate

# install the dependencies to the virtual environment
pip install -r requirements.txt

# run it
./play

# build it
./build
```

Backlog
=======

  * Monster AI (moving, attacking, fleeing, ...)
  * Multiple dungeon devels (stairs up and down)
  * Character creation (race, role, stats, weapons, ...)
  * Main menu (new, load, about, quit)
  * Items items items
  * Combat system based on player stats
  * Stats get infected by items
  * Keyboard settings (vi, z/y, numpad, ...)
  * Makefile instead of build (bash) script
  * Have a brilliant idea for a title
  * Write a quickstart guide for
      - the game  (how to play)
      - development (venv, mypy, ...) (how to dev)
  * Implement write ui/ui_pygame.py
      - maybe rewrite the whole ui interface.
      - ASCII in pygame
      - Pixel graphic in pygame
  * Find good ECS dokumentation online
      - create a *Links* section in this file
  * Comments comments comments
  * ...


Journal
=======

  |   Date   |  Feature                                                      |
  |   :--:   |  :--                                                          |
  |2017-10-04| *Starting this File.* Not a big Deal, the big Deal will be, keeping it up to date!|
  |2017-10-05| Rendering System, Graphics Component, Code Cleanup, Tilemap Drawing,|
  |2017-10-06| Moving Directions NW, N, NE, E, SE, S, SW, W Enum auto() for Commands (custom auto() for py < 3.6) Renamed System: Moving --> Turn Renamed Component: Moving --> MoveOrAttack|
  |2017-10-09| Implemented entities_at_position() in Turn System (not the best and final location of that function!) Refactored is_blocked() to use entities_at_position() Implemented a Quick and Dirty Very Basic! Move or Attack logic.|
  |2017-10-15| Implemented a helper function classes_from_module().  components module now has a components.all_components member.  Fixed some visibility errors.  Changed MoveOrAttack handling to an add/remove logic, like Door always was (remove component from entity instead of setting dxdy to (0, 0)).  Removed MapInteraction System. Extended Turn System. Turn System now has a _call_sub() method.|
  |2017-11-01| Implemented the StateManager and a State base class. the StateManager handles the main loop. Moved the try-finally around the curses initialization/uninitialization to the main file (roguelike.py). The Game class now is a State.|
  |2018-01-29| Tried to understand my (not so old) Code. Started to implement a Menu.|
|2018-02-01| Restructured this README file.|



Version History
===============

   ---------- ----------- -----------------------------------------------------
      Date      Version   Feature
   ---------- ----------- -----------------------------------------------------
     (WIP)        v0.0    - Curses (Terminal) "Graphics"

                          - Random Singele Dungeon Level Generation

                          - Field Of View and Line Of Sight

                          - Basic Movement (vi-Keys + zu/bn) (German Keyboard!)

                          - Doors (open/close)

                          - Combat

                          - Main Menu

   ---------- ----------- -----------------------------------------------------



