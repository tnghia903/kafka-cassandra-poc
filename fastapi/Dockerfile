FROM python:3.9-slim

WORKDIR /app

COPY . .
RUN pip install --no-cache-dir -r requirements.txt
CMD ["fastapi", "run", "app/main.py", "--port", "80"]