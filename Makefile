###--CODE--#############################################################################################################

format:
	ruff check --fix ./src/crosszoo/ && ruff format ./src/crosszoo/

lint:
	ruff check ./src/crosszoo/ && \
		ruff format --check ./src/crosszoo/ && \
		mypy --install-types --non-interactive ./src/crosszoo/

########################################################################################################################
