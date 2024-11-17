# docker/sso-gateway/Dockerfile

FROM python:3.12-slim

WORKDIR /app

# Install dependencies
COPY requirements.txt .
COPY requirements-devel.txt .
RUN pip install --no-cache-dir -r requirements.txt -r requirements-devel.txt


COPY app app
COPY config config

# Expose application and debug ports
EXPOSE 8000

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]

# Modify CMD to include debugpy for debugging
# EXPOSE 5678
# CMD ["python", "-m", "debugpy", "--listen", "0.0.0.0:5678", "--wait-for-client", "-m", "uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
