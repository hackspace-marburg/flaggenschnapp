FROM python:3-slim

COPY main.py requirements.txt /
COPY data /data
RUN /usr/local/bin/python -m pip install --upgrade pip \
		pip install -r requirements.txt

CMD python3 -u main.py
