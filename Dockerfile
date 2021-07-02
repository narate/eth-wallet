FROM python:alpine

RUN apk add --update --no-cache gcc musl-dev
WORKDIR /app
ADD requirements.txt .
RUN pip install -r requirements.txt
ADD create-wallet.py .
WORKDIR /db
ENTRYPOINT ["python", "/app/create-wallet.py"]
