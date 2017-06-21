#/bin/sh

nohup redis-server &
cd /home/renyafeng/embedding/google_vectors/
nohup python3 s1.py &
cd /home/renyafeng/code/work/flask/test1/
nohup gunicorn -b 0.0.0.0:8093 --worker-class=gevent -t 99999 t2:app &

