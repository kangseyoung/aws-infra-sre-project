# Runbook: MiniPEP Container Down

## Scenario
MiniPEP container is stopped, unhealthy, or not serving `/health`.

Nginx may be used only for early network connectivity tests. The final service target is the MiniPEP FastAPI application.

## Symptoms
- `curl -i http://localhost/health` fails
- Docker container is exited
- ALB health check fails
- ALB Target Group is unhealthy

## Check Order
1. Check Docker service status
2. Check running containers with `docker ps -a`
3. Review MiniPEP container logs
4. Verify host `80` to container `8000` port mapping
5. Confirm EC2 has enough disk and memory
6. Confirm required environment variables and SQLite DB path are valid
7. Confirm no unnecessary container ports are exposed

## Resolution Steps
- Restart Docker service if needed
- Re-run the MiniPEP container
- Rebuild the image if the container image is invalid
- Fix application configuration or environment variables if startup fails
- Restore the expected port mapping if it changed

## Record Items
- Detection time:
- Container name:
- Image tag:
- `curl -i http://localhost/health` result:
- Log evidence:
- Root cause:
- Resolution time:
