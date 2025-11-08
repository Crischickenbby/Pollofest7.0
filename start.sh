#!/bin/bash
pip uninstall -y psycopg2 psycopg2-binary
pip install psycopg2-binary==2.9.9 --force-reinstall --no-cache-dir
exec gunicorn --bind 0.0.0.0:$PORT app:app