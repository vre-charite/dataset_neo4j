FROM python:3.7-buster
USER root
WORKDIR /usr/src/app
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
CMD ["bash", "-c", "source /vault/secrets/config && ./gunicorn_starter.sh"]
# CMD ["python","app.py"]
