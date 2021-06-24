
.PHONY: help
help:
	@printf "\033[36m%-30s\033[0m %-50s %s\n" "[Sub command]" "[Description]" "[Example]"
	@grep -E '^[/a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | perl -pe 's%^([/a-zA-Z_-]+):.*?(##)%$$1 $$2%' | awk -F " *?## *?" '{printf "\033[36m%-30s\033[0m %-50s %s\n", $$1, $$2, $$3}'


.PHONY: test-python
test-python: ## test python ## make test-python
	pytest ./test -vv --cov=./pyargent --cov-report=html


.PHONY: deploy
deploy: ## deploy to PyPI ## make deploy
	twine upload dist/*


.PHONY: test-deploy
test-deploy: ## deploy to test-PyPI ## make test-deploy
	twine upload -r testpypi dist/*


.PHONY: wheel
wheel: clean ## generate wheel ## make wheel
	python setup.py sdist bdist_wheel


.PHONY: clean
clean: ## remove all files in dist ## make clean
	rm -f -r pyargent.egg-info/* dist/* -y


.PHONY: build
build: ## build image ## make build
	@docker build -t python/streamlit .


.PHONY: start
start: ## start local ## make start
	@docker run -p 8001:8001 -it python/streamlit streamlit run app.py