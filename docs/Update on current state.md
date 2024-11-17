# Update on current state

## File Layout:

```
.flake8
.gitignore
.isort.cfg
Dockerfile
README.md
app/auth/dependencies.py
app/auth/exceptions.py
app/auth/keycloak.py
app/auth/token_dependencies.py
app/auth/token_refresh.py
app/context.py
app/context_manager.py
app/main.py
app/models/tables.py
app/models/token.py
app/routes/__init__.py
app/routes/api.py
app/routes/auth.py
app/routes/error.py
app/routes/home.py
app/routes/protected.py
app/routes/tokens.py
app/static/css/bootstrap.min.css
app/static/js/bootstrap.bundle.min.js
app/templates/home.html
app/utils/config.py
app/utils/config_manager.py
app/utils/logger.py
app/utils/sessions.py
app/utils/tokens.py
app/utils/url_helpers.py
config/config_example.yaml
config/secrets_example.yaml
db/.gitignore
docker-compose.yml
docker/README.md
docker/apache-proxy/proxy.conf
docker/docker-compose.yml
docker/dummy-api/Dockerfile
docker/dummy-api/app/main.py
docker/dummy-api/requirements.txt
docker/sso-gateway/Dockerfile
docs/1. Task SSO integration for Legacy App.md
docs/2. Technical Specifications for SSO Integration.md
docs/3. SSO Integration Design.md
docs/4. Integration Test Setup.md
docs/design.webp
requirements.txt
tests/test_example.py
```


```yaml
# docker/docker-compose.yml

version: '3.8'
services:
  apache-proxy:
    build:
      context: ./apache-proxy
      dockerfile: Dockerfile
    container_name: apache-proxy
    ports:
      - "80:80"
    volumes:
      - ./apache-proxy/proxy.conf:/usr/local/apache2/conf/extra/proxy.conf:ro
    depends_on:
      - sso-gateway
    networks:
      - app-network

  sso-gateway:
    build:
      context: ..
      dockerfile: docker/sso-gateway/Dockerfile
    container_name: sso-gateway
    volumes:
      - ./sso-gateway/config:/app/config:ro
      - ./sso-gateway/db:/app/db
    environment:
      - TZ=Europe/Moscow
    ports:
      - "8000:8000"
      - "5678:5678"  # Debug port
    depends_on:
      - dummy-api
    networks:
      - app-network

  dummy-api:
    build:
      context: ./dummy-api
      dockerfile: Dockerfile
    container_name: dummy-api
    ports:
      - "5000:5000"
    networks:
      - app-network

networks:
  app-network:
    driver: bridge
```

```
# docker/sso-gateway/Dockerfile

FROM python:3.12-slim

WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
RUN pip install debugpy

COPY . .

# Expose application and debug ports
EXPOSE 8000 5678

# Modify CMD to include debugpy for debugging
CMD ["python", "-m", "debugpy", "--listen", "0.0.0.0:5678", "--wait-for-client", "-m", "uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]  # <-- [change]
```

```
# docker/dummy-api/Dockerfile

FROM python:3.12-slim

WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
RUN pip install debugpy

# Copy application code
COPY . .

# Expose application and debug ports
EXPOSE 5000 5678

# Modify CMD to include debugpy for debugging
CMD ["python", "-m", "debugpy", "--listen", "0.0.0.0:5678", "--wait-for-client", "-m", "uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "5000"]  # <-- [change]
```

```
# docker/apache-proxy/Dockerfile

FROM httpd:2.4

# Enable necessary Apache modules
RUN sed -i '/#LoadModule proxy_module modules\/mod_proxy.so/s/^#//g' /usr/local/apache2/conf/httpd.conf
RUN sed -i '/#LoadModule proxy_http_module modules\/mod_proxy_http.so/s/^#//g' /usr/local/apache2/conf/httpd.conf
RUN sed -i '/#LoadModule headers_module modules\/mod_headers.so/s/^#//g' /usr/local/apache2/conf/httpd.conf

# Copy the custom proxy configuration to the extra directory
COPY proxy.conf /usr/local/apache2/conf/extra/proxy.conf

# Include the custom proxy configuration in the main httpd.conf
RUN echo "Include conf/extra/proxy.conf" >> /usr/local/apache2/conf/httpd.conf

# Expose the default HTTP port
EXPOSE 80
```

```python
# docker/dummy-api/app/main.py

from fastapi import FastAPI, Header, HTTPException

app = FastAPI()

@app.get("/api/data")
async def get_data(x_remote_user: str = Header(None)):
    if not x_remote_user:
        raise HTTPException(status_code=401, detail="Unauthorized")
    return {"message": f"Hello, {x_remote_user}!"}

@app.post("/api/data")
async def post_data(data: dict, x_remote_user: str = Header(None)):
    if not x_remote_user:
        raise HTTPException(status_code=401, detail="Unauthorized")
    return {"message": f"Data received from {x_remote_user}", "data": data}
```
