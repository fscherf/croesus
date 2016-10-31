Test Project
------------

Install
~~~~~~~

::

    $ cd test_project
    $ virtualenv -p python3.4 env
    $ source env/bin/activate
    (env) $ pip install -r REQUIREMENTS.txt
    (env) $ ./manage.py migrate
    (env) $ ./manage.py createsuperuser
