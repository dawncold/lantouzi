#! /bin/bash

set -e

venv/bin/python main.py
git checkout gh-pages
cp posts/stats-year-2020.json .
git add stats-year-2020.json
git commit -m "update data"
git push
git checkout master