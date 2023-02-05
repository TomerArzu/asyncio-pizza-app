FROM python:3.10-slim-buster


LABEL maintainer="Tomer Arzuan <YouNeedToKnow@MyEmailAddress.com>" \
      image="pizza-app"

WORKDIR /app

COPY . /app

RUN pip install --no-cache-dir -r requirements.txt

ENV PYTHONUNBUFFERED 1

EXPOSE 5000

CMD ["python", "main.py"]