FROM python:3.11-slim
LABEL authors="sindhu"

WORKDIR /app

COPY . /app

ENV PYTHONPATH=/app

RUN pip install --no-cache-dir -r requirements.txt

ENTRYPOINT ["python","src/scanner.py"]

# set default argument
CMD ["nodejs/node"]