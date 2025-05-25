FROM python:3.13-alpine
RUN pip install "gunicorn"
ADD . /nya
WORKDIR /nya
RUN pip install "."
ENV NYA_SETTINGS /data/settings.py
CMD ["gunicorn", "-b 0.0.0.0:80", "-w 4", "nya_app:app"]
