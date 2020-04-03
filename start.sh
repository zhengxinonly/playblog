#! /bin/bash
cd /home/xxp/playblog
source venv/bin/activate
exec gunicorn -c gunicorn.conf.py app:app