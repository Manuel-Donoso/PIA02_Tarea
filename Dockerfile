FROM python:3.9-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
# Usamos -u para ver los prints en tiempo real en la consola de Docker
CMD ["python", "-u", "main.py"]