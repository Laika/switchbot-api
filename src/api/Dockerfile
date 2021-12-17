FROM python:3.10-slim
ENV PYTHONUNBUFFERED=1


RUN pip install --no-cache-dir -U pip

WORKDIR /app
COPY requirements.txt /app/
RUN pip install --no-cache-dir -r /app/requirements.txt

COPY . /app
CMD ["uvicorn", "api:app", "--host", "0.0.0.0", "--reload"]
