PYTHON_VERSION=python3.4
ENV_NAME=env
DB_NAME=db.sqlite3

.PHONY: clean full-clean db

all: db

clean:
	rm -rf $(ENV_NAME)

full-clean: clean
	rm -rf $(DB_NAME) django mt940

django:
	git clone https://github.com/django/django.git -b stable/1.8.x

mt940:
	git clone https://github.com/WoLpH/mt940.git -b v4.2

env: django mt940
	virtualenv -p $(PYTHON_VERSION) $(ENV_NAME) && \
	. env/bin/activate && \
	pip install \
		-e django \
		django-debug-toolbar \
		django-extensions \
		pyyaml \
		ipython \
		flake8 \
		-e mt940 \
		-e ..

db: env
	rm -rf $(DB_NAME)
	. env/bin/activate && \
	./manage.py migrate && \
	./manage.py loaddata user_data.json
