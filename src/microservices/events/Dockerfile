FROM python:3.12-slim
COPY ./requirements.txt /app/requirements.txt
WORKDIR /app
RUN apt-get update && apt-get install -y \
    librdkafka-dev \
    gcc \
    g++ \
    && rm -rf /var/lib/apt/lists/*
RUN pip install -r requirements.txt
COPY . /app
ENTRYPOINT ["python"]
CMD ["main.py"]

