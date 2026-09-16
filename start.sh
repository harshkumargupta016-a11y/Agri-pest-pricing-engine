#!/bin/bash
# Launch the production server
gunicorn api.main:app -c gunicorn_conf.py
