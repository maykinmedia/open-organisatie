#!/bin/bash

set -e -o pipefail  # exit on errors

echo "[INIT] Create project directory"

cd myproject

echo "[INIT] Create virtual environment"
virtualenv env --python=/usr/bin/python3
source env/bin/activate
python -V

echo "[INIT] Start new Django project based on template"
env/bin/pip install uv
uv pip install django
mkdir -p foo
django-admin startproject \
    --template=https://bitbucket.org/maykinmedia/default-project/get/master.zip  \
    --extension=py,rst,html,gitignore,json,ini,js,sh,cfg,yml,example,sql,toml \
    --name Dockerfile foobar foo

echo "[INIT] Create pinned requirements"
cd foo
git init
./bin/compile_dependencies.sh

echo "[INIT] Done."
deactivate

echo "[INSTALL] Typical first steps in the new project"
# python bootstrap.py jenkins
# Replaced bootstrap.py with classic commands:
source ../env/bin/activate
uv pip install -r requirements/dev.txt
export DJANGO_SETTINGS_MODULE=foobar.conf.jenkins
# End classic commands.
../env/bin/python src/manage.py collectstatic --link --noinput
# python src/manage.py migrate --noinput
../env/bin/python src/manage.py check
deactivate

echo "[JENKINS] Execute test suite"
../env/bin/python src/manage.py test src \
  --verbosity 2 \
  --noinput
