# MiniPEP

MiniPEP is a small FastAPI demo application for the AWS infrastructure/SRE project. It gives the EC2 Docker host a realistic application to run behind an AWS Application Load Balancer.

The original static Nginx page was useful for initial infrastructure testing. For the final demo app, Nginx has been replaced by this FastAPI MiniPEP service.

This first version intentionally does not include authentication, React, RDS, CI/CD, Terraform changes, ECS, Kubernetes, Prometheus, or Grafana.

## Deployment Contract

| Item | Value |
| --- | --- |
| App server | Uvicorn |
| Container port | `8000` |
| Host port | `80` |
| Docker mapping | `80:8000` |
| ALB Target Group port | `80` |
| Health check path | `/health` |
| Expected health response | HTTP `200` |

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
uvicorn minipep.main:app --host 0.0.0.0 --port 8000
```

On Windows PowerShell:

```powershell
cd app
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
uvicorn minipep.main:app --host 0.0.0.0 --port 8000
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
app/data/minipep.db
```

The app creates the database automatically and seeds sample equipment and jobs when the database is empty.
