#
# Makefile for __N_A_M_E__
#
# targets:
#
#   docs  ->  creates html files in docs/ from md files in docs-src/
#             the docs/ dir is the github page.
#             TODO: configure github to use the docs/ dir as the github.io page.
#
#   clean  -> removes all files generatable by this make file
#

NAME=roguelike

DOC-CC=pandoc
PY-CC=pyinstaller

DOC-SRC-DIR=docs-src
DOC-DIR=docs
VIRTUALENV=venv

BIN-DIR=bin
SRC-DIR=src
TMP-DIR=tmp
SRC-FILE=$(SRC-DIR)/$(NAME).py

PY-CC-FLAGS=--clean --onefile --srtip
DOC-FLAGS=--from=markdown --to=html --standalone --smart

DOC-SRC-FILES=$(wildcard $(DOC-SRC-DIR)/*.md)
DOC-FILES=$(patsubst $(DOC-SRC-DIR)/%.md, $(DOC-DIR)/%.html, $(DOC-SRC-FILES))


default:
	source $(VIRTUALENV)/bin/activate
	$(PY-CC) $(PY-CC-FLAGS) --workpath=$(TMP-DIR) --distpath=$(BIN-DIR) $(SRC-FILE)
	deactivate
	rm -r $(TMP-DIR)
	rm $(NAME).spec


$(DOC-DIR)/%.html: $(DOC-SRC-DIR)/%.md
	$(DOC-CC) --output=$@ $(DOC-FLAGS) $<


.PHONY: docs
docs: $(DOC-FILES)

.PHONY: clean
clean:
	rm -r $(DOC-DIR)
	rm -r $(BIN-DIR)

