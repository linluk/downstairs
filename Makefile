#
# Makefile for __N_A_M_E__
#
# targets:
#
#   docs  ->  creates html files in docs/ from md files in docs-src/
#             the docs/ dir is the github page.
#             TODO: configure github to use the docs/ dir as the github.io page.
#                   but first: find a name !!! and renam the repository.
#
#   clean  -> removes all files generatable by this make file
#

NAME=downstairs

VIRTUALENV=venv
DOC-CC=pandoc
PY-CC=python -OO $(VIRTUALENV)/bin/pyinstaller

DOC-SRC-DIR=docs-src
DOC-DIR=docs

BIN-DIR=bin
SRC-DIR=src
TMP-DIR=tmp
SRC-FILE=$(SRC-DIR)/roguelike.py

PY-CC-FLAGS=--clean --onefile --strip --log-level=WARN --specpath $(TMP-DIR)
DOC-FLAGS=--from=markdown --to=html --standalone --smart

DOC-SRC-FILES=$(wildcard $(DOC-SRC-DIR)/*.md)
DOC-FILES=$(patsubst $(DOC-SRC-DIR)/%.md, $(DOC-DIR)/%.html, $(DOC-SRC-FILES))


default:
	( \
	  . $(VIRTUALENV)/bin/activate ; \
	  $(PY-CC) $(PY-CC-FLAGS) --workpath=$(TMP-DIR) --distpath=$(BIN-DIR) --name $(NAME) $(SRC-FILE) ; \
	  deactivate ; \
	)


$(DOC-DIR)/%.html: $(DOC-SRC-DIR)/%.md
	$(DOC-CC) --output=$@ $(DOC-FLAGS) $<


.PHONY: docs
docs: $(DOC-FILES)

.PHONY: clean
clean:
	rm  $(DOC-DIR)/*
	rm  $(BIN-DIR)/*
	rm -r $(TMP-DIR)

