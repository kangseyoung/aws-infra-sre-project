# Runbook: ALB Health Check Failure

## Scenario
ALB target health shows unhealthy or MiniPEP is not reachable through the load balancer.

## Symptoms
- Target Group shows unhealthy targets
- Browser access to ALB fails
- `http://ALB-DNS/health` does not return HTTP 200
- CloudWatch basic metric shows unhealthy hosts

## Check Order
1. Confirm the target is registered in the correct Target Group
2. Verify the health check path is `/health`
3. Verify the Target Group protocol and port are HTTP `80`
4. Verify the EC2 host listens on `80` and forwards to the MiniPEP container on `8000`
5. Confirm EC2 security group allows HTTP `80` only from the ALB security group
6. Check Docker and MiniPEP status on EC2
7. Run `curl -i http://localhost/health` inside EC2
8. Review Docker stdout and MiniPEP Application Log
9. Review ALB listener and forwarding rule

## Resolution Steps
- Fix health check path if it is not `/health`
- Update security group rules if ALB cannot reach EC2
- Restart or rebuild the MiniPEP container if the service is down
- Re-register target if instance association is incorrect
- Restore the expected port mapping if EC2 `80` does not reach container `8000`

## Record Items
- Detection time:
- Failing target ID:
- Health check path / port:
- EC2 internal `/health` result:
- Docker / MiniPEP log evidence:
- Root cause:
- Resolution time:
