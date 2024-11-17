# Docker Development Environment for SSO Gateway

This directory contains the Docker Compose setup for the SSO Gateway, Apache Reverse Proxy, and Dummy REST API. It includes configurations for debugging using `debugpy` and integration with VSCode.

## Table of Contents

- [Docker Development Environment for SSO Gateway](#docker-development-environment-for-sso-gateway)
  - [Table of Contents](#table-of-contents)
  - [Prerequisites](#prerequisites)
  - [Directory Structure](#directory-structure)
  - [Building and Running Containers](#building-and-running-containers)
  - [Connecting the Debugger with VSCode](#connecting-the-debugger-with-vscode)
    - [VSCode Launch Configuration](#vscode-launch-configuration)
  - [Using `curl` to Interact with SSO Gateway](#using-curl-to-interact-with-sso-gateway)
    - [Access Home Page](#access-home-page)
    - [Login](#login)
    - [Logout](#logout)
    - [Token Management](#token-management)
      - [Add Token](#add-token)
      - [List Tokens](#list-tokens)
      - [Revoke Token](#revoke-token)
  - [Additional Instructions](#additional-instructions)
    - [Notes](#notes)

## Prerequisites

- [Docker](https://www.docker.com/get-started) installed on your machine.
- [Docker Compose](https://docs.docker.com/compose/install/) installed.
- [VSCode](https://code.visualstudio.com/) with the Python extension installed (for debugging).

## Directory Structure

```
project/
├── docker/
│   ├── README.md
│   ├── docker-compose.yml
│   ├── apache-proxy/
│   │   ├── Dockerfile
│   │   └── proxy.conf
│   ├── sso-gateway/
│   │   ├── Dockerfile
│   │   └── config/
│   │       ├── config.yaml
│   │       └── secrets.yaml
│   └── dummy-api/
│       ├── Dockerfile
│       └── app/
│           └── main.py
├── app/
│   └── ... (existing application code)
└── .vscode/
    └── launch.json
```

## Building and Running Containers

1. **Navigate to the `docker/` Directory:**

   ```bash
   cd docker/
   ```

2. **Build and Start the Containers:**

   ```bash
   docker-compose up --build -d
   ```

   - The `--build` flag ensures that Docker rebuilds the images with the latest changes.
   - The `-d` flag runs the containers in detached mode.

3. **Verify the Containers are Running:**

   ```bash
   docker-compose ps
   ```

   You should see `apache-proxy`, `sso-gateway`, and `dummy-api` services listed as up.

## Connecting the Debugger with VSCode

To debug both the `sso-gateway` and `dummy-api` services using VSCode, follow these steps:

### VSCode Launch Configuration

1. **Create a `.vscode/launch.json` File:**

   In the root of your project (not inside the `docker/` directory), create a `.vscode/launch.json` file with the following content:

   ```json
   {
       "version": "0.2.0",
       "configurations": [
           {
               "name": "Attach to SSO Gateway",
               "type": "python",
               "request": "attach",
               "connect": {
                   "host": "localhost",
                   "port": 5678
               },
               "pathMappings": [
                   {
                       "localRoot": "${workspaceFolder}/docker/sso-gateway",
                       "remoteRoot": "/app"
                   }
               ]
           },
           {
               "name": "Attach to Dummy API",
               "type": "python",
               "request": "attach",
               "connect": {
                   "host": "localhost",
                   "port": 5678
               },
               "pathMappings": [
                   {
                       "localRoot": "${workspaceFolder}/docker/dummy-api",
                       "remoteRoot": "/app"
                   }
               ]
           }
       ]
   }
   ```

2. **Start Debugging:**

   - Open the **Run and Debug** view in VSCode (`Ctrl+Shift+D`).
   - Select **Attach to SSO Gateway** or **Attach to Dummy API** from the dropdown.
   - Click the **Start Debugging** button.

   Ensure that the Docker containers are running and that ports `5678` are exposed as per the Dockerfile configurations.

## Using `curl` to Interact with SSO Gateway

Here are some example `curl` commands to interact with the SSO Gateway. Replace `http://localhost` with your actual gateway URL if different.

### Access Home Page

```bash
curl -v http://localhost/gateway/
```

### Login

Initiate the login process:

```bash
curl -v http://localhost/gateway/auth/login?next=http://localhost/gateway/
```

- This will redirect you to the Keycloak login page. Since it's a `curl` request, you won't see the actual login page, but you can observe the redirect headers.

### Logout

Assuming you have a valid session/token, you can log out:

```bash
curl -v http://localhost/gateway/auth/logout?next=http://localhost/gateway/
```

### Token Management

#### Add Token

Generate a new API token:

```bash
curl -X POST http://localhost/gateway/tokens/generate -b cookies.txt -c cookies.txt
```

- `-b cookies.txt` and `-c cookies.txt` are used to send and store cookies for session management.

#### List Tokens

Retrieve the list of tokens:

```bash
curl http://localhost/gateway/tokens/ -b cookies.txt -c cookies.txt
```

#### Revoke Token

Revoke a specific token:

```bash
curl -X DELETE http://localhost/gateway/tokens/revoke/<TOKEN> -b cookies.txt -c cookies.txt
```

- Replace `<TOKEN>` with the actual token string you wish to revoke.

## Additional Instructions

For more detailed instructions, troubleshooting, and advanced configurations, refer to the [Top-Level README.md](../README.md).

---

### Notes

- **Environment Variables and Secrets:**
  - Ensure that sensitive information like `client_secret` is stored securely in `secrets.yaml` and not hardcoded.
  - The `secrets.yaml` file should **not** be committed to version control systems.

- **Debugging:**
  - When attaching the debugger, ensure that your VSCode workspace is correctly mapped to the Docker container's file system using the `pathMappings` in `launch.json`.

- **API Access:**
  - The Dummy REST API is configured to require the `X-Remote-User` header for authentication. Ensure that requests proxied through the SSO Gateway include this header.

- **Cache Control:**
  - The application is configured to prevent caching of sensitive pages to ensure that authentication status changes are accurately reflected.

- **Running Without Docker:**
  - If you need to run the services outside of Docker for debugging or other purposes, ensure that the `redirect_uri` in `config.yaml` matches the external URL accessible by Keycloak.
