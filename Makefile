.PHONY: activate_venv run_server run_client run

# To ensure the venv exists, each of the recipes is depending on the $(VENV) target,
# which ensures we always have an up-to-date venv installed.
# This works, because the . venv/bin/activate-script basically just does the same:
# it puts the venv before anything else in your PATH,
# therefore each call to python, etc. will find the one installed in the venv first.
VENV = venv
BIN=$(VENV)/bin
PY = python3  # system python interpreter. used only to create virtual environment
PIP = $(BIN)/pip
PYTHON = $(BIN)/python3

# make it work on windows too
ifeq ($(OS), Windows_NT)
    BIN=$(VENV)/Scripts
    PY=python
endif


activate_venv: $(BIN)/activate

$(BIN)/activate: requirements.txt
	test -d $(VENV) || virtualenv -p python3 $(VENV)
	${PYTHON} -m pip install -U pip
	${PYTHON} -m pip install -r requirements.txt
	touch $(BIN)/activate



run_server: activate_venv
	$(PY) run_server.py


run_client: activate_venv
	$(PY) run_client.py


run: activate_venv
	$(PY) __init__.py


clean:
	rm -rf $(VENV)
	rm -rf .pytest_cache
	rm -rf __pycache__
	find . -type f -name *.pyc -delete
	find . -type d -name __pycache__ -delete