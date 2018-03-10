README
======

Author: Lukas Singer, Daniel Nimmervoll

Created: 2017-10-04

License: [WTFPL](http://www.wtfpl.net/)

This project should become a
[Roguelike](http://en.wikipedia.org/wiki/Roguelike) Game.

It was renamed from `roguelike` to **`downstairs`** on 2018-03-10.

Setup
=====

```
# clone the repository
git clone https://github.com/linluk/downstairs.git
cd downstairs

# prepare it (virtual enviroment and requirements):
make venv

# run it (from source files)
./play_ascii
# or ./play_cmdln if you prefere to play in terminal

# build it
make
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


