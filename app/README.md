# MiniPEP

MiniPEP is a small FastAPI demo application for the AWS infrastructure/SRE project. It gives the EC2 Docker host a realistic application to run behind an AWS Application Load Balancer.

The original static Nginx page was useful for initial infrastructure testing. For the final demo app, Nginx has been replaced by this FastAPI MiniPEP service.

This first version intentionally does not include authentication, React, RDS, CI/CD, Terraform changes, ECS, Kubernetes, Prometheus, or Grafana.

## Deployment Contract

| Item | Value |
| --- | --- |
| Service name | MiniPEP |
| Runtime | Docker container |
| Framework | FastAPI/Uvicorn |
| App server | Uvicorn |
| Container Port | `8000` |
| EC2 Host Port | `80` |
| Docker mapping | `80:8000` |
| ALB Target Group Port | `80` |
| Health Check Path | `/health` |
| Expected Health Response | HTTP `200` |
| Main Page | `/` |
| Logs | stdout, view with `docker logs` or `docker compose logs` |
| Persistence | local SQLite under `/app/data` |

## Endpoints

| Method | Path | Purpose |
| --- | --- | --- |
| `GET` | `/` | Web dashboard |
| `GET` | `/health` | ALB health check |
| `GET` | `/api/equipment` | List equipment |
| `POST` | `/api/equipment` | Create equipment |
| `GET` | `/api/jobs` | List jobs |
| `POST` | `/api/jobs` | Create job |
| `PUT` | `/api/jobs/{job_id}` | Update job |
| `DELETE` | `/api/jobs/{job_id}` | Delete job |

## Local Python Run

From the repository root:

```bash
cd app
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python -m uvicorn minipep.main:app --host 0.0.0.0 --port 8000
```

On Windows PowerShell:

```powershell
cd app
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
python -m uvicorn minipep.main:app --host 0.0.0.0 --port 8000
```

Open:

```text
http://localhost:8000/
```

## Docker Build

From the repository root:

```bash
cd app
docker build -t minipep:latest .
```

## Docker Run

This maps host port `80` to container port `8000`.

```bash
docker run -d \
  --name minipep \
  -p 80:8000 \
  -v "$(pwd)/data:/app/data" \
  minipep:latest
```

On Windows PowerShell:

```powershell
docker run -d `
  --name minipep `
  -p 80:8000 `
  -v "${PWD}\data:/app/data" `
  minipep:latest
```

## Docker Compose

```bash
cd app
docker compose up -d --build
```

The compose file uses:

```text
ports:
  - "80:8000"
```

## Health Check

Local Python run:

```bash
curl -i http://localhost:8000/health
```

Docker or EC2 run through host port `80`:

```bash
curl -i http://localhost/health
```

Expected result:

```text
HTTP/1.1 200 OK
```

Example body:

```json
{"status":"ok","service":"minipep"}
```

## Verification Results

The following checks have been verified.

### Local FastAPI Run

Command:

```bash
cd app
python -m uvicorn minipep.main:app --host 0.0.0.0 --port 8000
```

Verified results:

* `GET /` returned the MiniPEP dashboard.
* `GET /health` returned HTTP `200 OK`.
* `GET /api/equipment` returned equipment data.
* `GET /api/jobs` returned job data.

### Docker Run

Commands:

```bash
cd app
docker build -t minipep:latest .
docker run -d --name minipep -p 80:8000 -v "$(pwd)/data:/app/data" minipep:latest
curl -i http://localhost/health
curl -i http://localhost/api/equipment
curl -i http://localhost/api/jobs
docker logs minipep
docker stop minipep
docker rm minipep
```

Windows PowerShell volume syntax:

```powershell
docker run -d --name minipep -p 80:8000 -v "${PWD}\data:/app/data" minipep:latest
```

Verified results:

* `http://localhost/health` returned HTTP `200 OK`.
* `http://localhost/api/equipment` returned equipment data.
* `http://localhost/api/jobs` returned job data.
* `docker logs minipep` showed request logs.
* `docker stop minipep` and `docker rm minipep` worked.

### Docker Compose

Commands:

```bash
cd app
docker compose up -d --build
curl -i http://localhost/health
curl -i http://localhost/api/equipment
curl -i http://localhost/api/jobs
docker compose logs minipep
docker compose down
```

Verified results:

* `docker compose up -d --build` succeeded.
* `http://localhost/health` returned HTTP `200 OK`.
* `http://localhost/api/equipment` returned equipment data.
* `http://localhost/api/jobs` returned job data.
* `docker compose logs minipep` showed request logs.
* `docker compose down` worked.

## Logs

MiniPEP logs every request and important create/update/delete actions to stdout.

Docker:

```bash
docker logs -f minipep
```

Docker Compose:

```bash
docker compose logs -f minipep
```

## EC2 Deployment Example

Install Docker on the EC2 instance, then clone the repository and run the app:

```bash
git clone <repo-url>
cd aws-infra-2week-project/app
docker compose up -d --build
curl -i http://localhost/health
docker compose logs -f minipep
```

Make sure the EC2 security group allows inbound traffic from the ALB security group to port `80`.

## ALB Target Group Example

Use these Target Group settings:

```text
Target type: Instances
Protocol: HTTP
Port: 80
Health check protocol: HTTP
Health check path: /health
Success codes: 200
```

Register the EC2 instance as a target on port `80`.

Request path:

```text
Client -> ALB:80 -> Target Group:80 -> EC2 host port 80 -> Docker container port 8000 -> Uvicorn/FastAPI
```

## SQLite Data

SQLite persists under:

```text
/app/data
```

The app creates the local SQLite database automatically and seeds sample equipment and jobs when the database is empty. Local SQLite database files under `app/data` are ignored by git and must not be committed.
