REQUIREMENTS_FILE = requirements.txt

install-dependencies:
	@pip3 install -r $(REQUIREMENTS_FILE) --break-system-packages

run:
	@if [ -z "$(input)" ]; then echo "input file path is required"; exit 1; fi
	@if [ -z "$(output)" ]; then echo "output file path is required"; exit 1; fi
	@if [ -z "$(verbose)" ]; then echo "verbose level is required"; exit 1; fi
	@python3 main.py $(input) $(output) $(verbose) > log.txt

setup: install-dependencies

visualize:
	@python3 visualizer.py $(input) $(output)

.PHONY: install-dependencies run setup
