FROM python:3.10-slim-bullseye

WORKDIR /app

COPY src/requirements.txt /app/requirements.txt

RUN pip install --no-cache-dir -r requirements.txt

COPY src/ /app/

EXPOSE 8000

CMD ["python", "-m", "uvicorn", "api.main:app", "--host", "0.0.0.0", "--port", "8000"]