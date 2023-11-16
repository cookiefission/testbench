.PHONY: env
env: ## Creates the default virtual environment to run.
	pyenv uninstall -f testbench-opgaai
	pyenv virtualenv 3.12.0 testbench-opgaai

.PHONY: reqs
reqs: ## Generates the requirements.txt file without installing the dependencies.
	pip install --upgrade pip pip-tools
	pip-compile --no-emit-index-url --resolver=backtracking

.PHONY: deps
deps: reqs ## Installs dependencies needed to run the project.
	pip-sync requirements.txt

