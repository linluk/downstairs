#
# Makefile for DOWNSTAIRS the roguelike
#
# Author: Lukas Singer
#
# Created: 2018-03-09
#


#################
#               #
# CONFIGURATION #
#               #
#################


# the name of the game
NAME=downstairs

# the directory for the virtual enviroment
# HINT: dont change this, this is also a targets name!
VIRTUALENV=venv

# the "compiler" for the docs
DOC-CC=pandoc

# the "compiler" for the game (the executable)
PY-CC=python -OO $(VIRTUALENV)/bin/pyinstaller

# the "compiler" for the build info
BUILD-INFO-CC=python tools/generate_build_info.py

# the source and destination directories for the docs
DOC-SRC-DIR=docs-src
# HINT: dont change this, this is also a targets name and
#       the name of the gh-pages!
DOC-DIR=docs

# the source and destination directory for the game (the executable)
SRC-DIR=src
BIN-DIR=bin

# the temp dir (f.e. for creating the docs or creating the executable)
TMP-DIR=tmp

# the build info file
BUILD-INFO-FILE=$(SRC-DIR)/build_info.py

# the main source file
SRC-FILE=$(SRC-DIR)/roguelike.py

# the docs source and destination files
DOC-SRC-FILES=$(wildcard $(DOC-SRC-DIR)/*.md)
DOC-FILES=$(patsubst $(DOC-SRC-DIR)/%.md, $(DOC-DIR)/%.html, $(DOC-SRC-FILES))

# the images for the docs
DOC-SRC-IMAGES=$(wildcard $(DOC-SRC-DIR)/images/*.png)
DOC-IMAGES=$(patsubst $(DOC-SRC-DIR)/images/%.png, $(DOC-DIR)/images/%.png, $(DOC-SRC-IMAGES))

# the requirements file
REQ-FILE=requirements.txt

# activation and deactivation commands for the virtual enviroment
ACTIVATE-VIRTUALENV=. $(VIRTUALENV)/bin/activate
DEACTIVATE-VIRTUALENV=deactivate

# flags for the "compiler" for the game
PY-CC-FLAGS=--clean --onefile --strip --log-level=WARN --specpath $(TMP-DIR)

# flags for the "compiler" for the docs
DOC-FLAGS=--from=markdown --to=html --standalone --smart


###########
#         #
# TARGETS #
#         #
###########


# build the game when invoked with:
#   $ make
default:
	( \
	  $(ACTIVATE-VIRTUALENV) ; \
	  $(BUILD-INFO-CC) --output=$(BUILD-INFO-FILE) ; \
	  $(PY-CC) $(PY-CC-FLAGS) --workpath=$(TMP-DIR) --distpath=$(BIN-DIR) --name $(NAME) $(SRC-FILE) ; \
	  $(DEACTIVATE-VIRTUALENV) ; \
	)


# create the virtual enviroment and install requirements when invoked with:
#   $ make venv
.PHONY: $(VIRTUALENV)
$(VIRTUALENV):
	( \
	  python3 -m venv $(VIRTUALENV) ; \
	  $(ACTIVATE-VIRTUALENV) ; \
	  pip install -r $(REQ-FILE) ; \
	  $(DEACTIVATE-VIRTUALENV) ; \
	)

# remove the virtual enviroment when invoked with:
#   $ make clean-venv
clean-venv:
	rm -r $(VIRTUALENV)


# build the docs when invoked with:
#   $ make docs
.PHONY: $(DOC-DIR)
$(DOC-DIR): $(DOC-FILES) $(DOC-IMAGES)

$(DOC-DIR)/%.html: $(DOC-SRC-DIR)/%.md
	mkdir -p $(DOC-DIR)
	$(DOC-CC) --output=$@ $(DOC-FLAGS) $<

$(DOC-DIR)/images/%.png: $(DOC-SRC-DIR)/images/%.png
	mkdir -p $(DOC-DIR)/images
	ln --force --physical $< $@


# remove everything created with this Makefile (except the virtual enviroment) when invoked with:
#   $ make clean
.PHONY: clean
clean:
	rm -r $(DOC-DIR)
	rm -r $(BIN-DIR)
	rm -r $(TMP-DIR)
	rm $(BUILD-INFO-FILE)

