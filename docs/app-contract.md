# MiniPEP App Contract

This document defines the deployment contract between the MiniPEP application and the AWS infrastructure.

## Service

| Item | Value |
| --- | --- |
| Service name | MiniPEP |
| Runtime | Docker container |
| Framework | FastAPI/Uvicorn |
| Container Port | `8000` |
| EC2 Host Port | `80` |
| ALB Target Group Port | `80` |
| Health Check Path | `/health` |
| Health Check Expected Response | HTTP `200` |
| Main Page | `/` |
| Logs | stdout, view with `docker logs` or `docker compose logs` |
| Persistence | local SQLite under `/app/data` |

## Traffic Flow

```text
Client -> ALB:80 -> Target Group:80 -> EC2 host port 80 -> Docker container port 8000 -> FastAPI/Uvicorn
```

## Required Commands

### Local Run

```bash
cd app
python -m uvicorn minipep.main:app --host 0.0.0.0 --port 8000
```

### Docker Build

```bash
cd app
docker build -t minipep:latest .
```

### Docker Run

```bash
cd app
docker run -d --name minipep -p 80:8000 -v "$(pwd)/data:/app/data" minipep:latest
```

Windows PowerShell volume syntax:

```powershell
cd app
docker run -d --name minipep -p 80:8000 -v "${PWD}\data:/app/data" minipep:latest
```

### Docker Compose Up

```bash
cd app
docker compose up -d --build
```

### Health Check

Local FastAPI run:

```bash
curl -i http://localhost:8000/health
```

Docker, Docker Compose, or EC2 host port:

```bash
curl -i http://localhost/health
```

Expected response:

```text
HTTP/1.1 200 OK
```

## Logs

Docker:

```bash
docker logs minipep
```

Docker Compose:

```bash
docker compose logs minipep
```

## Persistence

MiniPEP persists local SQLite data under `/app/data` inside the container. During local Docker or Compose runs, `app/data` is mounted to `/app/data`.

Local SQLite database files under `app/data` are ignored by git and must not be committed.
