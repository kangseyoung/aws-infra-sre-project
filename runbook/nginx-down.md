# Runbook: Nginx Down

## Scenario
Nginx container is stopped, unhealthy, or not serving the test page.

## Symptoms
- `curl localhost` fails
- Docker container is exited
- ALB health check fails

## Check Order
1. Check Docker service status
2. Check running containers with `docker ps -a`
3. Review container logs
4. Verify Nginx config and port mapping
5. Confirm EC2 has enough disk and memory

## Resolution Steps
- Restart Docker service if needed
- Re-run the Nginx container
- Rebuild the image if the container image is invalid
- Fix the Nginx config if startup fails

## Record Items
- Detection time:
- Container name:
- Image tag:
- Root cause:
- Resolution time:

