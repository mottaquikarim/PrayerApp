SHELL := /bin/bash
app = prayerapp

clean:
	## TODO address when we lack perms to delete these
	find . -name __pycache__ -prune -exec rm -fr {} \;
	find . -name "*.pyc" -exec rm -fr {} \;
	find . -name .eggs -prune -exec rm -fr {} \;
	find . -name "*.egg-info" -prune -exec rm -fr {} \;
	rm -fr build/ dist/
	## Kill pytest_cache for good measure
	rm -rf .pytest_cache
	## fix for file import error...
	rm -rf ./test/__pycache__

dist:
	docker-compose run prayerapp-dist

build-dev: dist
	docker-compose build ${app}

test: build-dev
	docker-compose run ${app} /test.sh

test-dev: test

## Mainly local dev helper, runs a lot faster for quick
## syntax updates, etc
quick-test: clean
	## activating shell cmd in make;
	## ref: https://stackoverflow.com/a/24736236/8285967
	( \
		source .venv/bin/activate; \
		pip install --trusted-host None --no-index --find-links ./dist prayerapp; \
		pytest ./test; \
		deactivate; \
	)
